import asyncio
import colorama
import concurrent
import git
# mypy fails with 'error: Trying to read deleted variable "exc"' if we use
# 'git.exc'
import git.exc as gitexc
import glob
import os
import psutil
import pyprctl
import random
import resemble.rc as rc
import subprocess
import sys
import threading
from contextlib import asynccontextmanager, contextmanager
from grpc_tools import protoc as grpc_tools_protoc
from importlib import resources
from resemble.monkeys import monkeys, no_chaos_monkeys
from resemble.rc import fail, info, warn
from resemble.settings import ENVOY_PROXY_IMAGE
from typing import AsyncIterator, Iterable, Optional, Set
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver


@asynccontextmanager
async def watch(
    paths: list[str]
) -> AsyncIterator[asyncio.Task[FileSystemEvent]]:
    """Helper for watching the provided paths on file system. Implemented
    as a context manager to ensure proper cleanup of the watches."""
    loop = asyncio.get_running_loop()

    class EventHandler(FileSystemEventHandler):

        def __init__(self, events: asyncio.Queue[FileSystemEvent]):
            self._events = events

        def on_modified(self, event):
            loop.call_soon_threadsafe(lambda: self._events.put_nowait(event))

    events: asyncio.Queue[FileSystemEvent] = asyncio.Queue()

    handler = EventHandler(events)

    observer: Optional[BaseObserver] = None

    while True:
        # Construct a new observer everytime to avoid re-adding the
        # same path and raising an error.
        observer = Observer()

        try:
            # We want to (re)determine the paths to watch _every_ time
            # to find any new subdirectories added by the developer
            # which they surely expect we will properly watch as well.
            for unglobed_path in paths:
                has_globbed_paths = False
                for path in glob.iglob(unglobed_path, recursive=True):
                    has_globbed_paths = True

                    if not os.access(path, os.R_OK):
                        fail('Expecting path passed to --watch to be readable')

                    observer.schedule(handler, path=path, recursive=False)

                if not has_globbed_paths:
                    warn(f"'{unglobed_path}' did not match any files")

            observer.start()
            break
        except:
            # NOTE: we capture all exceptions here because
            # 'observer.schedule()' may raise if a file that we had
            # globbed gets removed before calling it (e.g., by a build
            # system) and we just want to retry since the build system
            # should be completing and not removing files out from
            # underneath us all the time.
            await asyncio.sleep(0.5)
            continue

    # Ok, should have a valid observer now!
    assert observer is not None

    events_get = asyncio.create_task(events.get())

    try:
        yield events_get
    finally:
        events_get.cancel()
        observer.stop()
        observer.join()


async def terminate(process: subprocess.Popen | asyncio.subprocess.Process):
    """Helper for terminating a process and all of its descendants.

    This is non-trivial to do as processes may have double forked and
    are no longer part of the process tree, but there are a handful of
    different mechanisms that we document extensively within the
    implementation for how we try and kill all possible descedants of
    a process.
    """
    while True:
        # Try and get all the processes descendants first, before we
        # try and terminate it and lose the process tree.
        descendants = set()

        # (1) Add processes with same PGID as 'process'.
        #
        # This gets all processes that 'process' created that did not
        # create a new process group, even if they double forked and
        # are no longer direct descendants of 'process'.
        try:
            pgid = os.getpgid(process.pid)
        except ProcessLookupError:
            # Process might have already exited, e.g., because it
            # crashed, or we already killed it.
            #
            # Use the PID as PGID as they should be the same since
            # when the process was created it created a new process
            # group whose ID is the same as the PID.
            pgid = process.pid

        for p in psutil.process_iter():
            try:
                if os.getpgid(p.pid) == pgid:
                    descendants.add(p)
            except ProcessLookupError:
                # Process might have already exited, e.g., because it
                # crashed, or we already killed it.
                pass

        # (2) Add descendants of 'process'.
        #
        # This gets processes that might have changed their process
        # group but are still descendants of 'process'.
        try:
            for p in psutil.Process(process.pid).children(recursive=True):
                descendants.add(p)
        except psutil.NoSuchProcess:
            # Process 'process' might have already exited, e.g.,
            # because it crashed, or we already killed it.
            pass

        # Send SIGTERM to the process _but not_ the descendants to let
        # it try and clean up after itself first.
        #
        # Give it some time, but not too much time, before we try and
        # terminate everything.
        try:
            process.terminate()
            await asyncio.sleep(0.1)
        except ProcessLookupError:
            # Process might have already exited, e.g., because it
            # crashed, or we already killed it.
            pass

        # (3) Add _our_ descendants that have a different PGID.
        #
        # On Linux when we enable the subreaper so any processes that
        # both changed their process group and tried to double fork so
        # that they were no longer a descendant of 'process' should
        # now be a descendant of us however they will be in a
        # different process group than us.
        #
        # Note that while using the subreaper on Linux implies that
        # (3) subsumes (1), because the subreaper is best effort (as
        # in, we don't rely on having the requisite capabilities to
        # use the subreaper), we include them both.
        pgid = os.getpgid(os.getpid())

        for p in psutil.Process(os.getpid()).children(recursive=True):
            try:
                if os.getpgid(p.pid) != pgid:
                    descendants.add(p)
            except ProcessLookupError:
                # Process 'p' might have already exited, e.g., because
                # it crashed or we already killed it (but it actually
                # exited after it was determined one of our children).
                pass

        # Don't try and terminate ourselves! This can happen when we
        # try and terminate any processes that we were not able to put
        # into a separate process group.
        descendants = set(
            [
                descendant for descendant in descendants
                if descendant.pid != os.getpid()
            ]
        )

        if len(descendants) == 0:
            break

        for descendant in descendants:
            try:
                descendant.terminate()
            except psutil.NoSuchProcess:
                # Process might have already exited, e.g., because it
                # crashed, or we already killed it.
                pass

        _, alive = psutil.wait_procs(descendants, timeout=1)

        for descendant in alive:
            try:
                descendant.kill()
            except psutil.NoSuchProcess:
                # Process might have already exited, e.g., because
                # it crashed, or we already killed it.
                pass

        # Can wait forever here because a process can't ignore kill.
        psutil.wait_procs(alive)


@asynccontextmanager
async def run(application, *, env: dict[str, str], launcher: Optional[str]):
    """Helper for running the application with an optional launcher."""
    process = await asyncio.create_subprocess_exec(
        application,
        # NOTE: starting a new sesssion will also put the
        # process into its own new process group. Each time we
        # restart the application we need to kill all
        # processes which are not in our process group as that
        # implies that they are processes that were created by
        # the application or one of its descendants.
        start_new_session=True,
        env=env,
    ) if launcher is None else await asyncio.create_subprocess_exec(
        launcher,
        application,
        # NOTE: see comment above on sessions.
        start_new_session=True,
        env=env,
    )
    try:
        yield process
    finally:
        await terminate(process)


default_local_envoy_port: int = 9991


def dot_rsm_directory() -> str:
    """Helper for determining the '.rsm' directory."""
    try:
        repo = git.Repo(search_parent_directories=True)
    except gitexc.InvalidGitRepositoryError:
        return os.path.join(os.getcwd(), '.rsm')
    else:
        return os.path.join(repo.working_dir, '.rsm')


def dot_rsm_dev_directory() -> str:
    """Helper for determining the '.rsm/dev' directory."""
    return os.path.join(dot_rsm_directory(), 'dev')


async def run_background_command(
    background_command: str,
    *,
    print_as: Optional[str] = None,
):
    info(f"Running background command '{print_as or background_command}'")
    process = await asyncio.create_subprocess_shell(background_command)
    try:
        await process.wait()
    except asyncio.CancelledError:
        await terminate(process)
    else:
        if process.returncode != 0:
            fail(
                f"Failed to run background command '{background_command}', "
                f"exited with {process.returncode}"
            )
        else:
            warn(
                f"Background command '{background_command}' exited without errors"
            )


@contextmanager
def chdir(directory):
    """Context manager that changes into a directory and then changes back
    into the original directory before control is returned."""
    cwd = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cwd)


@contextmanager
def use_working_directory(
    working_directory: str,
    parser: rc.ArgumentParser,
):
    """Context manager that changes into a working directory determined by
    how the parser expanded any flags."""
    for expanded_flag in parser.expanded_flags:
        if expanded_flag.startswith('--working-directory'):
            assert parser.dot_rc is not None
            with chdir(os.path.dirname(parser.dot_rc)):
                working_directory = os.path.abspath(working_directory)
                break

    info(f"Using working directory {working_directory}\n")

    with chdir(working_directory):
        yield


def is_on_path(file):
    """Helper to check if a file is on the PATH."""
    for directory in os.environ['PATH'].split(os.pathsep):
        if os.path.exists(os.path.join(directory, file)):
            return True
    return False


async def dev(args, *, parser: rc.ArgumentParser):
    """Implementation of the 'dev' subcommand."""
    # Determine the working directory and move into it.
    with use_working_directory(args.working_directory, parser):
        application = os.path.abspath(args.application)

        # If on Linux try and become a child subreaper so that we can
        # properly clean up all processes descendant from us!
        if sys.platform == 'linux':
            try:
                pyprctl.set_child_subreaper(True)
            except:
                warn(
                    "Failed to become child subreaper, we'll do our "
                    "best to ensure all created processes are terminated"
                )
                pass

        # Run any background commands.
        background_command_tasks: list[asyncio.Task] = []

        for background_command in args.background_command or []:
            background_command_tasks.append(
                asyncio.create_task(
                    run_background_command(background_command)
                )
            )

        if args.protoc_watch:
            # Run `rsm protoc` _once_, so that the application doesn't
            # exit because it can't find any of the generated files.
            #
            # Using `sys.argv[0]` in the event that `rsm` is
            # not on the path or someone renamed it.
            #
            # TODO(benh): aggregate all of the `--config=` and pass
            # them on to `rsm protoc`.
            rsm_protoc = f'{sys.executable} {sys.argv[0]} protoc'

            process = await asyncio.create_subprocess_shell(rsm_protoc)

            try:
                await process.wait()
            except asyncio.CancelledError:
                await terminate(process)
            else:
                if process.returncode != 0:
                    fail(
                        "Failed to run 'rsm protoc' "
                        "(you can disable this with --no-protoc-watch)"
                    )

            background_command_tasks.append(
                asyncio.create_task(
                    run_background_command(
                        f'{rsm_protoc} --watch --wait-for-changes',
                        print_as='rsm protoc --watch --wait-for-changes',
                    )
                )
            )

        # Set all the environment variables that
        # 'resemble.aio.Application' will be looking for.

        os.environ['RSM_DEV'] = 'true'

        if args.name is not None:
            os.environ['RSM_DEV_NAME'] = args.name
            os.environ['RSM_DOT_RSM_DEV_DIRECTORY'] = dot_rsm_dev_directory()

        if args.local_envoy:
            # Check if Docker is running and can access the Envoy proxy image.
            # fails otherwise.
            await _check_docker_status()
            os.environ['RSM_DEV_LOCAL_ENVOY'] = 'true'
        else:
            os.environ['RSM_DEV_LOCAL_ENVOY'] = 'false'

        os.environ['RSM_DEV_LOCAL_ENVOY_PORT'] = str(
            args.local_envoy_port or default_local_envoy_port
        )

        if not args.chaos:
            warn(
                '\n' + random.choice(no_chaos_monkeys) + '\n'
                'You Have Disabled Chaos Monkey! (see --chaos)\n'
                '\n'
                'Only You (And Chaos Monkey) Can Prevent Bugs!'
                '\n'
            )

        env_copy = os.environ.copy()

        for (key, value) in args.env or []:
            env_copy[key] = value

        try:
            while True:
                if args.name is None:
                    warn(
                        '\n'
                        'Starting an ANONYMOUS application; to reuse state '
                        'across application restarts use --name'
                        '\n'
                    )

                # It's possible that the application may get deleted
                # and then (re)created by a build system so rather
                # than fail if we can't find it we'll retry but print
                # out a warning every ~10 seconds (which corresponds
                # to ~20 retries since we sleep for 0.5 seconds
                # between each retry).
                retries = 0
                while not os.path.isfile(application):
                    if retries != 0 and retries % 20 == 0:
                        warn(
                            f"Missing application at '{application}' "
                            "(is it being rebuilt?)"
                        )
                    retries += 1
                    await asyncio.sleep(0.5)

                # Expect an executable if we haven't been asked to use
                # `python`.
                if (
                    args.python is None and
                    not os.access(application, os.X_OK)
                ):
                    fail(
                        f"Expecting executable application at '{application}'"
                    )

                async with watch(
                    [application] + (args.watch or [])
                ) as file_system_event_task:
                    # TODO(benh): catch just failure to create the subprocess
                    # so that we can either try again or just listen for a
                    # modified event and then try again.
                    async with run(
                        application,
                        env=env_copy,
                        launcher=sys.executable
                        if args.python is not None else None,
                    ) as process:
                        process_wait_task = asyncio.create_task(process.wait())

                        if args.chaos:
                            chaos_task = asyncio.create_task(
                                asyncio.sleep(random.randint(30, 60))
                            )

                        completed, pending = await asyncio.wait(
                            [file_system_event_task, process_wait_task] +
                            ([chaos_task] if args.chaos else []),
                            return_when=asyncio.FIRST_COMPLETED,
                        )

                        # Cancel chaos task regardless of what task
                        # completed first as we won't ever wait on it.
                        if args.chaos:
                            chaos_task.cancel()

                        task = completed.pop()

                        if task is process_wait_task:
                            warn(
                                '\n'
                                'Application exited unexpectedly '
                                '... waiting for modification'
                                '\n'
                            )
                            # NOTE: we'll wait for a file system event
                            # below to signal a modification!
                        elif args.chaos and task is chaos_task:
                            warn(
                                '\n'
                                'Chaos Monkey Is Restarting Your Application'
                                '\n' + random.choice(monkeys) + '\n'
                                '... disable via --no-chaos if you must'
                                '\n'
                                '\n'
                            )
                            continue

                        file_system_event: FileSystemEvent = await file_system_event_task

                        info(
                            '\n'
                            'Application modified; restarting ... '
                            '\n'
                        )
        except:
            if len(background_command_tasks) > 0:
                for background_command_task in background_command_tasks:
                    background_command_task.cancel()

                await asyncio.wait(
                    background_command_tasks,
                    return_when=asyncio.ALL_COMPLETED,
                )

            raise


async def protoc(
    args,
    argv_after_dash_dash: list[str],
    parser: rc.ArgumentParser,
):
    """Invokes `protoc` with the arguments passed to 'rsm protoc'."""
    # Determine the working directory and move into it.
    with use_working_directory(args.working_directory, parser):

        async def install_protoc_gen_es():
            """Helper to install 'protoc-gen-es' and its dependencies.

            We install these in the '.rsm' directory, by placing an
            empty 'package.json' file and then running 'npm install'
            as necessary. This approach makes it so that we don't have
            to bundle 'protoc-gen-es' as part of our pip package.

            """
            if not is_on_path('npm'):
                fail(
                    "We require 'npm' and couldn't find it on your PATH. "
                    "Is it installed?"
                )

            if not is_on_path('node'):
                fail(
                    "We require 'node' and couldn't find it on your PATH. "
                    "Is it installed?"
                )

            os.makedirs(dot_rsm_directory(), exist_ok=True)

            with chdir(dot_rsm_directory()):
                if (
                    not os.path.isfile('package.json') or
                    os.path.getsize('package.json') == 0
                ):
                    with open('package.json', 'w') as file:
                        file.write("{}")

                async def shell(command):
                    """Helper for running shell commands to install all of the
                    dependencies of 'protobuf-gen-es'. We redirect
                    stdout/stderr to a pipe and only print it out if
                    the command fails.

                    """
                    process = await asyncio.create_subprocess_shell(
                        command,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.STDOUT,
                    )

                    stdout, _ = await process.communicate()

                    if process.returncode != 0:
                        fail(
                            "\n"
                            f"{command}: "
                            "\n"
                            f"{stdout.decode()}\n"
                            "\n"
                            "Failed to install 'protoc-gen-es'. "
                            "Please report this bug to the maintainers."
                        )

                await shell(f'npm install @bufbuild/protobuf')
                await shell(f'npm install @bufbuild/protoc-gen-es')

        # Fill in `protoc` args based on our args.
        protoc_args: list[str] = ["grpc_tool.protoc"]

        # Add 'protoc-gen-es' plugin.
        await install_protoc_gen_es()

        protoc_args.append(
            f"--plugin={os.path.join(dot_rsm_directory(), 'node_modules', '.bin', 'protoc-gen-es')}"
        )

        # We want to find the Python `site-packages`/`dist-packages` directories
        # that contain a 'resemble/v1alpha1' directory, which is where we'll
        # find our protos. We can look for the 'resemble' folder via the
        # `resources` module; the resulting path is a `MultiplexedPath`, since
        # there may be multiple. Such a path doesn't contain a `parent`
        # attribute, since there isn't one answer. Instead we use `iterdir()` to
        # get all of the children of all 'resemble' folders, and then
        # deduplicate the parents-of-the-parents-of-those-children (via the
        # `set`), which gives us the `resemble` folders' parents' paths.
        resemble_parent_paths: set[str] = set()
        for path in resources.files('resemble').iterdir():
            resemble_parent_paths.add(str(path.parent.parent))

        if len(resemble_parent_paths) == 0:
            raise FileNotFoundError(
                "Failed to find 'resemble' resource path. "
                "Please report this bug to the maintainers."
            )

        # Now add these to '--proto_path', so that users don't need to provide
        # their own Resemble protos.
        for resemble_parent_path in resemble_parent_paths:
            protoc_args.append(f"--proto_path={resemble_parent_path}")

        # User protos may rely on `google.protobuf.*` protos. We
        # conveniently have those files packaged in our Python
        # package; make them available to users, so that users don't
        # need to provide them.
        protoc_args.append(
            f"--proto_path={resources.files('grpc_tools').joinpath('_proto')}"
        )

        # Now set flags, e.g., '--python_out' '--grpc_python_out',
        # '--resemble_out', etc, to `args.output_directory` if they
        # are not already specified explicitly.
        def user_specified_explicit(arg: str):
            """Helper for checking if the user explicitly specified an argument."""
            return any(
                [
                    protoc_arg.startswith(arg)
                    for protoc_arg in argv_after_dash_dash
                ]
            )

        output_directory = args.output_directory

        plugins_using_output_directory: Set[str] = set()

        python_output: Optional[str] = None

        if not user_specified_explicit('--python_out'):
            protoc_args.append(f'--python_out={output_directory}')
            plugins_using_output_directory.add("'python'")
        else:
            # Determine the value of '--python_out'. It may come in
            # the form '--python_out=VALUE' or '--python_out VALUE'.
            for i in range(len(argv_after_dash_dash)):
                protoc_arg = argv_after_dash_dash[i]
                if protoc_arg.startswith('--python_out'):
                    python_output = protoc_arg
                    if '=' not in python_output:
                        if len(argv_after_dash_dash) - 1 == i:
                            fail(
                                'Missing value for --python_out, try '
                                '--python_out=path/to/directory'
                            )
                        else:
                            python_output = argv_after_dash_dash[i + 1]
                    else:
                        python_output = python_output.split('=', 1)[1]

        if not user_specified_explicit('--grpc_python_out'):
            if python_output is None:
                protoc_args.append(f'--grpc_python_out={output_directory}')
                plugins_using_output_directory.add("'python'")
            else:
                protoc_args.append(f'--grpc_python_out={python_output}')

        if not user_specified_explicit('--resemble_out'):
            if python_output is None:
                protoc_args.append(f'--resemble_out={output_directory}')
                plugins_using_output_directory.add("'python'")
            else:
                protoc_args.append(f'--resemble_out={python_output}')

        if not user_specified_explicit('--es_out'):
            protoc_args.append(f'--es_out={output_directory}')
            plugins_using_output_directory.add("'react'")

        if len(plugins_using_output_directory) == 0:
            warn(
                f"Ignoring --output-directory={args.output_directory} in favor "
                "favor of the explicitly specified output directories set after --\n"
            )

        # TODO(benh): in the future only generate the following
        # warning if we are not using the output directory for ALL of
        # the files that we are generating.
        if len(plugins_using_output_directory) > 0:
            warn(
                f"Using output directory '{output_directory}' "
                f"for generated {', '.join(plugins_using_output_directory)} files. "
                "Use '--output-directory=DIRECTORY' to override it "
                "(or use the `protoc` args, e.g., '--python_out=DIRECTORY', to "
                "explicitly specify output for particular languages or plugins).\n"
            )
            os.makedirs(output_directory, exist_ok=True)

        # Add all args after '--'.
        protoc_args += argv_after_dash_dash

        # Grab all of the positional '.proto' arguments.
        proto_directories: list[str] = args.proto_directories or []

        protos = []

        for proto_directory in proto_directories:
            # Expand any directories to be shortform for 'directory/**/*.proto'.
            if not os.path.isdir(proto_directory):
                fail(f"Failed to find directory '{proto_directory}'")
            else:
                # Also add any directories given to us as part of the import path.
                protoc_args.append(f'--proto_path={proto_directory}')
                found_protos = False
                for file in glob.iglob(
                    os.path.join(proto_directory, '**', '*.proto'),
                    recursive=True,
                ):
                    _, extension = os.path.splitext(file)
                    if extension == '.proto':
                        found_protos = True
                        protos.append(file)

                if not found_protos:
                    fail(
                        f"'{proto_directory}' did not match any '.proto' files"
                    )

        protoc_args += protos

        if not is_on_path('protoc-gen-resemble'):
            raise FileNotFoundError(
                "Failed to find 'protoc-gen-resemble'. "
                "Please report this bug to the maintainers."
            )

        # Indicates whether or not we should wait for changes to
        # '.proto' files initially or run immediately. We'll reuse
        # this variable for watching below.
        wait_for_changes = args.wait_for_changes

        while True:
            if wait_for_changes:
                async with watch(protos) as file_system_event_task:
                    await file_system_event_task

            if not args.verbose:
                info(
                    'Running `protoc ...` (use --verbose to see full command)'
                )
            else:
                info('protoc')
                for arg in protoc_args[1:]:
                    info(f'  {arg}')

            returncode = grpc_tools_protoc.main(protoc_args)

            if not args.watch:
                sys.exit(returncode)
            else:
                wait_for_changes = True

                # Print a new line between each invocation.
                print()

                continue


async def _check_docker_status():
    """Checks if Docker is running and can use the Envoy proxy image. Downloads
    that image if necessary."""

    async def _subprocess_exec(*args, **kwargs) -> tuple[int, str]:
        """Helper that invokes a subprocess, sends `stderr` to `stdout`,
        and returns (returncode, stdout)."""
        try:
            process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                **kwargs,
            )
        except FileNotFoundError:
            # If the executable is not accessible 'create_subprocess_exec'
            # will raise an error before the process is created.
            executable = args[0]
            return -1, f"We require '{executable}' and we couldn't find it on your PATH. Is it installed?"
        else:
            output, _ = await process.communicate()
        assert process.returncode is not None
        return process.returncode, output.decode()

    returncode, output = await _subprocess_exec("docker")
    if returncode != 0:
        fail(output)

    # The '-q' flag returns only the image ID, so if stdout is empty
    # then the image is not downloaded.
    returncode, output = await _subprocess_exec(
        "docker", "images", "-q", ENVOY_PROXY_IMAGE
    )
    if returncode != 0:
        fail(
            f"Could not use Docker; 'docker images -q {ENVOY_PROXY_IMAGE}' failed with output:\n{output}"
        )

    # Empty output means the image is not downloaded. ('Docker' didn't find a
    # match for the image name.)
    if output == "":
        info(f"Pulling Envoy proxy image '{ENVOY_PROXY_IMAGE}'...")
        returncode, output = await _subprocess_exec(
            "docker", "pull", ENVOY_PROXY_IMAGE
        )
        if returncode != 0:
            fail(
                f"Could not use Docker; 'docker pull {ENVOY_PROXY_IMAGE}' failed with output:\n{output}"
            )


class EnvTransformer(rc.BaseTransformer):

    def transform(self, value: str):
        if '=' not in value:
            raise rc.TransformerError(
                f"Invalid flag '--env={value}': must be in the form "
                "'--env=KEY=VALUE'"
            )
        return value.split('=', 1)


def create_parser(
    *,
    rc_file: Optional[str] = None,
    argv: Optional[list[str]] = None,
) -> rc.ArgumentParser:
    parser = rc.ArgumentParser(
        program='rsm',
        filename='.rsmrc',
        subcommands=['dev', 'protoc'],
        rc_file=rc_file,
        argv=argv,
    )

    parser.subcommand('dev').add_argument(
        '--working-directory',
        type=str,
        help="directory in which to execute",
        required=True,
    )

    parser.subcommand('dev').add_argument(
        '--name',
        type=str,
        help="name of instance; state will be persisted using this name in "
        f"'{dot_rsm_dev_directory()}'",
    )

    parser.subcommand('dev').add_argument(
        '--background-command',
        type=str,
        repeatable=True,
        help=
        'command(s) to execute in the background (multiple instances of this '
        'flag are supported)',
    )

    parser.subcommand('dev').add_argument(
        '--local-envoy',
        type=bool,
        default=True,
        help='whether or not to bring up a local Envoy'
    )

    parser.subcommand('dev').add_argument(
        '--local-envoy-port',
        type=int,
        help=f'port for local Envoy; defaults to {default_local_envoy_port}',
    )

    parser.subcommand('dev').add_argument(
        '--python',
        type=bool,
        default=False,
        help="whether or not to launch the application by "
        "passing it as an argument to 'python'",
    )

    parser.subcommand('dev').add_argument(
        '--watch',
        type=str,
        repeatable=True,
        help=
        'path to watch; multiple instances are allowed; globbing is supported',
    )

    parser.subcommand('dev').add_argument(
        '--chaos',
        type=bool,
        default=True,
        help='whether or not to randomly induce failures',
    )

    parser.subcommand('dev').add_argument(
        "--env",
        type=str,
        repeatable=True,
        transformer=EnvTransformer(),
        help=
        "sets any specified environment variables before running the application; "
        "'ENV' should be of the form 'KEY=VALUE'",
    )

    parser.subcommand('dev').add_argument(
        "--protoc-watch",
        type=bool,
        default=True,
        help=
        "by default, we also run `rsm protoc --watch`; pass --no-protoc-watch to disable"
    )

    parser.subcommand('dev').add_argument(
        'application',
        type=str,  # TODO: consider argparse.FileType('e')
        help='path to application to execute',
    )

    parser.subcommand('protoc').add_argument(
        '--working-directory',
        type=str,
        help="directory in which to execute",
        required=True,
    )

    parser.subcommand('protoc').add_argument(
        '--output-directory',
        type=str,
        help="output directory in which `protoc` will generate files",
        required=True,
    )

    parser.subcommand('protoc').add_argument(
        '--watch',
        type=bool,
        default=False,
        help="watches specified 'protos' for changes and re-runs `protoc`"
    )

    parser.subcommand('protoc').add_argument(
        '--wait-for-changes',
        type=bool,
        default=False,
        help="wait for any changes to '.proto' files before running `protoc'"
    )

    parser.subcommand('protoc').add_argument(
        '--verbose',
        type=bool,
        default=False,
        help="whether or not to be verbose"
    )

    parser.subcommand('protoc').add_argument(
        'proto_directories',
        type=str,
        help="proto directory(s) which will (1) be included as import paths "
        "and (2) be recursively searched for '.proto' files to compile",
        repeatable=True,
        required=True,
    )

    return parser


async def rsm():
    colorama.init()

    parser = create_parser()

    args, argv_after_dash_dash = parser.parse_args()

    if args.subcommand == 'dev':
        await dev(args, parser=parser)
    elif args.subcommand == 'protoc':
        await protoc(args, argv_after_dash_dash, parser=parser)


# This is a separate function (rather than just being in `__main__`) so that we
# can refer to it as a `script` in our `pyproject.rsm.toml` file.
def main():
    try:
        asyncio.run(rsm())
    except KeyboardInterrupt:
        # Don't print an exception and stack trace if the user does a
        # Ctrl-C.
        pass


if __name__ == '__main__':
    main()
