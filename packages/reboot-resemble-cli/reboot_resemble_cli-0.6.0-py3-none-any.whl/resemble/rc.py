import argparse
import git
# mypy fails with 'error: Trying to read deleted variable "exc"' if we use
# 'git.exc'
import git.exc as gitexc
import os
import re
import shlex
import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from colorama import Fore, Style
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Iterable, Optional


# TODO(benh): move these helpers into a generic "CLI" module.
def info(message: str):
    if sys.stdout.isatty():
        print(
            Fore.GREEN + Style.BRIGHT + message + Style.RESET_ALL,
            file=sys.stdout,
        )
    else:
        print(message, file=sys.stdout)


def warn(message: str):
    if sys.stdout.isatty():
        print(
            Fore.YELLOW + Style.BRIGHT + message + Style.RESET_ALL,
            file=sys.stdout,
        )
    else:
        print(message, file=sys.stdout)


def fail(message: str):
    if sys.stderr.isatty():
        print(
            Fore.RED + Style.BRIGHT + message + Style.RESET_ALL,
            file=sys.stderr,
        )
    else:
        print(message, file=sys.stderr)
    sys.exit(1)


# Type aliases to help better understand types.
Subcommand = str
Config = str
Flag = str
Flags = defaultdict[tuple[Subcommand, Optional[Config]], list[Flag]]

# Regular expression patterns used for '.rc' file parsing.
#
# Pattern for subcommand, e.g., 'dev --some-flag and_args'.
SUBCOMMAND_PATTERN = r'^(\.\.\.|[-A-Za-z0-9]+)[ ].+$'

# Pattern for subcommand:config, e.g., 'dev:foo --some-flag and_args'.
SUBCOMMAND_CONFIG_PATTERN = r'^(\.\.\.|[-A-Za-z0-9]+):[-A-Za-z0-9]+[ ].+$'

# String representing flags for "common" expansion.
COMMON_PATTERN = '...'


class StoreOnceAction(argparse.Action):
    """Helper action that ensures that only one instance of a flag that is
    not meant to be repeated is present.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest) is not None:
            parser.error(
                f"found more than one instance of --{self.dest.replace('_', '-')}=VALUE"
            )
        else:
            setattr(namespace, self.dest, values)


class TransformerError(ValueError):
    """Raised when a transformer fails to transform a value."""

    def __init__(self, message: str):
        super().__init__(self, message)
        self.message = message


class BaseTransformer(ABC):
    """Base class a transformer.

    When an argument is being parsed, a transformer can modify the
    user-provided flag values to take a different shape than the original input.
    For example, a transformer could make all letters in a flag value uppercase,
    or could `'value,with,string,of,words'.split(',')`."""

    @abstractmethod
    def transform(self, value: str):
        raise NotImplementedError


class SubcommandParser:
    """Helper class that encapsulates an `argparse.ArgumentParser` so that
    we can control how arguments are added and to validate them for
    correctness and consistency with other args.
    """

    _parser: argparse.ArgumentParser

    _argument_types: dict[str, type]

    def __init__(self, parser: argparse.ArgumentParser):
        self._parser = parser
        self._argument_types: dict[str, type] = {}
        self._transformers: dict[str, Optional[BaseTransformer]] = {}

    def add_argument(
        self,
        name: str,
        *,
        type: type,
        help: str,
        repeatable: bool = False,
        required: Optional[bool] = None,
        default: Optional[Any] = None,
        transformer: Optional[BaseTransformer] = None,
    ):
        """Adds an argument. Unlike `argparse.ArgumentParser` this requires
        `type` and `help` so that we ensure we create a better
        experience for our end users.
        """
        if name.startswith('-') and not name.startswith('--'):
            raise ValueError(
                f"Invalid argument '{name}': flags must start "
                "with '--' not '-'"
            )

        if name.startswith('--') and '_' in name:
            raise ValueError(
                f"Invalid argument '{name}': flags must use kebab case"
            )

        if repeatable and default is not None:
            raise ValueError(
                f"Invalid argument '{name}': can not be "
                "'repeatable' and have a 'default'"
            )

        if repeatable and type == bool:
            raise ValueError(
                f"Invalid argument '{name}': 'bool' "
                "arguments can not be 'repeatable'"
            )

        kwargs: dict[str, Any] = {
            'type': type,
            'help': help,
        }

        if type == bool:
            kwargs['action'] = argparse.BooleanOptionalAction
        elif repeatable:
            if name.startswith('--'):
                # Repeated flags use the 'append' action.
                kwargs['action'] = 'append'
            else:
                # Repeated positional arguments use 'nargs'.
                if required:
                    kwargs['nargs'] = '+'
                else:
                    kwargs['nargs'] = '*'
        elif name.startswith('--'):
            kwargs['action'] = StoreOnceAction

        if name.startswith('--') and required is not None:
            kwargs['required'] = required

        if default is not None:
            kwargs['default'] = default

        self._parser.add_argument(name, **kwargs)

        self._argument_types[name] = type
        self._transformers[name] = transformer

    def get_argument_type(self, name: str) -> Optional[type]:
        """Helper that returns the type of an argument value."""
        return self._argument_types.get(name, None)

    def get_transformer(self, name: str):
        """Returns the specified argument's transformer or `None`."""
        return self._transformers.get(name, None)


class HelpFormatter(argparse.HelpFormatter):
    """Helper formatter that replaces all '--flag FLAG' with
    '--flag=FLAG'.
    """

    def format_help(self):
        # Get the default formatted help.
        help = super().format_help()

        # And replace all '--flag FLAG' with '--flag=FLAG'.
        return re.sub(r'(--[a-z-]+)[ ]([A-Z_]+)', r'\1=\2', help)


class ArgumentParser:
    """A CLI argument/options/flags parser that knows how to expand
    arguments found in a '.rc', e.g, '.rsmrc'.

    Formatting expected in a '.rc' file:

    (1) Comments. Any line starting with a '#' is skipped. All text
        after a trailling '#' is also dropped.

    (2) "Common" flags, i.e., flags that are relevant for all
        subcommands, defined by the top-level parser, are
        distinguished via a line that starts with '...':

        # Always expanded.
        ... --more-flags=42 and_args here

    (3) Subcommand specific flags:

        # Always expanded when invoking subcommand.
        subcommand --more-flags=42 and_args here

    (4) Config flags expanded from '--config=foo' for both "common"
        and subcommands:

        # Only expanded if --config=foo.
        ...:foo --flag=42
        subcommand:foo --more-flags=42

    (5) Recursive configs are fully supported:

        dev:fullstack --fullstack

        dev:demo --config=fullstack

    (6) All lines are aggregated.

        dev:demo --config=fullstack  # The demo is "fullstack".
        dev:demo --name=demo         # Name of demo.
        dev:demo --python            # Uses Python.


    TODO(benh): move this into own file 'rc_argument_parser.py'
    if/once we need it for other CLI tools.
    """

    def __init__(
        self,
        *,
        program: str,
        filename: str,
        subcommands: list[str],
        rc_file: Optional[str] = None,
        argv: Optional[list[str]] = None,
    ):
        self._parser = argparse.ArgumentParser(
            prog=program,
            allow_abbrev=False,
            # We need our own formatter class so we output
            # '--flag=FLAG' not '--flag FLAG'.
            formatter_class=HelpFormatter,
        )

        rsm_version = ''

        try:
            rsm_version = version('reboot-resemble-cli')
        except PackageNotFoundError as e:
            # If rsm is running in not-a-built-wheel-package.
            rsm_version = '<unreleased build>'

        self._parser.add_argument(
            '--version',
            action='version',
            version=rsm_version,
        )

        subparsers = self._parser.add_subparsers(
            dest='subcommand', required=True
        )

        self._subcommand_parsers: dict[str, SubcommandParser] = {}

        for subcommand in subcommands:
            subparser = subparsers.add_parser(
                subcommand,
                allow_abbrev=False,
                # We need our own formatter class so we output
                # '--flag=FLAG' not '--flag FLAG'.
                formatter_class=HelpFormatter,
            )

            # Ensure every subcommand has a '--config=' argument to
            # support configuration in '.rc' files. This is necessary
            # because `argparse` doesn't allow flags from the
            # top-level parser to be used after a subcommand, and we
            # want to allow users to do:
            #   `command subcommand --config=foo`
            # Not just:
            # `command --config=foo subcommand`
            subparser.add_argument(
                '--config',
                action='append',
                help=f"\"configs\" to apply from a '{filename}' file, "
                f"e.g., 'rsm {subcommand} --config=foo' would add all flags "
                f"on lines in the '{filename}' that start with '{subcommand}:foo'",
            )

            self._subcommand_parsers[subcommand] = SubcommandParser(subparser)

        argv = argv or list(sys.argv)

        self._argv_after_dash_dash = []

        try:
            dash_dash_index = argv.index('--')
        except ValueError:
            pass
        else:
            self._argv_after_dash_dash = argv[dash_dash_index + 1:]
            argv = argv[:dash_dash_index]

        self._help = '-h' in argv or '--help' in argv

        # Don't bother trying to expand args/flags from a '.rc' if the
        # user is asking for help because expanding args/flags means
        # calling `self._parser.parse_known_args(...)` and `argparse`
        # will see that '--help' or '-h' and print out a help message
        # that doesn't include all of the actual args/flags that will
        # get added after this constructor returns.
        if self._help:
            self.expanded_flags = []
            self._argv = argv
            self._subcommand = None
            return

        # Try to expand flags from a '.rc'
        #
        # NOTE: we must do this _before_ the rest of the arguments are
        # added because in order to properly expand flags for
        # subcommands we have to run the parser which will fail if we
        # are missing required arguments that are in fact not yet
        # expanded from the '.rc' file.
        if rc_file is not None:
            rc_file = os.path.abspath(rc_file)
            if not os.path.isfile(rc_file):
                fail(f"Failed to find {filename} at {rc_file}")
            if not os.access(rc_file, os.R_OK):
                fail(f"Found '{filename}' at {rc_file} but it is not readable")

        self.dot_rc: Optional[str] = (
            rc_file or ArgumentParser._find_dot_rc(filename)
        )

        if self.dot_rc is not None:
            expanded_flags, argv, subcommand = self._expand_dot_rc(
                filename,
                self.dot_rc,
                self._parser,
                subcommands,
                # NOTE: we get a copy of `sys.argv` so that it can be
                # referenced to try and determine where args/flags got
                # parsed from.
                argv,
            )
            self.expanded_flags = expanded_flags
            self._argv = argv
            self._subcommand = subcommand
        else:
            self.expanded_flags = []
            self._argv = argv

            # Determine the subcommand at this point so we can
            # validate that flags are always include an '=', e.g.,
            # '--flag=value'.
            known_args, _ = self._parser.parse_known_args(args=self._argv[1:])

            # Subcommands are required.
            assert known_args.subcommand is not None

            self._subcommand = known_args.subcommand

    def subcommand(self, subcommand: str):
        """Returns the parser for the specified subcommand."""
        if subcommand not in self._subcommand_parsers:
            raise ValueError(f"Invalid subcommand '{subcommand}'")
        return self._subcommand_parsers[subcommand]

    def parse_args(self):
        """Pass through to top-level parser with the expanded arguments after
        first validating that all flags include '=' between them and their value."""
        args = self._argv[1:]

        if self._help:
            return self._parser.parse_args(args=args)

        # We must have the subcommand at this point so that we can
        # call `self._get_argument_type(...)`.
        assert self._subcommand is not None

        # Ensure all non-boolean flags include '=', e.g.,
        # '--flag=value'.
        for i in range(len(args)):
            arg = args[i]
            if arg.startswith('--'):
                parts = arg.split('=', 1)
                assert len(parts) > 0
                arg_type: Optional[type] = self._get_argument_type(parts[0])

                if arg_type is None:
                    # Let `argparse` handle any invalid arguments.
                    continue

                if len(parts) == 1 and arg_type != bool:
                    # Try and guess what the user intended by printing
                    # out "did you mean {arg}={args[i + 1]" assuming
                    # that there is an `i + 1` argument.
                    did_you_mean = ""
                    if i + 1 < len(args):
                        quote = "'" if " " in args[i + 1] else ""
                        did_you_mean = f" (did you mean {arg}={quote}{args[i + 1]}{quote})"

                    self._parser.error(
                        f"expected {arg}=VALUE, missing '=VALUE'{did_you_mean}"
                    )

        namespace: argparse.Namespace = self._parser.parse_args(args=args)

        # Now let's apply any transformers to the parsed arguments.
        subcommand_parser = self._subcommand_parsers[self._subcommand]
        for name in vars(namespace):
            # After parsing, we have names without the '--' prefix. Since
            # we allow flags only with '--' prefix, we can add it back here,
            # to get the transformer.
            transformer = subcommand_parser.get_transformer('--' + name)
            if transformer is not None:
                value = getattr(namespace, name)
                if value is not None:
                    try:
                        if isinstance(value, list):
                            value = [transformer.transform(v) for v in value]
                        else:
                            value = transformer.transform(value)
                    except TransformerError as e:
                        self._parser.error(e.message)
                    else:
                        setattr(namespace, name, value)

        return namespace, self._argv_after_dash_dash

    def _get_argument_type(self, arg: str) -> Optional[type]:
        """Helper for getting an argument type from the correct parser given
        the subcommand that was determined during initialization."""
        # Subcommands are required when parsing, so we could not have
        # gotten here if we do not have a valid subcommand.
        assert self._subcommand is not None
        assert self._subcommand in self._subcommand_parsers

        return self._subcommand_parsers[self._subcommand
                                       ].get_argument_type(arg)

    @staticmethod
    def _find_dot_rc(filename: str) -> Optional[str]:
        """Tries to find the '.rc' file in the current directory or, if in a
        git repository, in the top-level directory of the repository,
        and returns the path if found otherwise `None`."""
        dot_rc: Optional[str] = None

        dot_rc = os.path.join(os.getcwd(), filename)
        if not os.path.isfile(dot_rc):
            try:
                repo = git.Repo(search_parent_directories=True)
            except gitexc.InvalidGitRepositoryError:
                return None
            else:
                dot_rc = os.path.join(repo.working_dir, filename)
                if not os.path.isfile(dot_rc):
                    return None

        assert dot_rc is not None

        if not os.access(dot_rc, os.R_OK):
            fail(f"Found '{filename}' at {dot_rc} but it is not readable")

        return os.path.abspath(dot_rc)

    @staticmethod
    def _read_flags_from_dot_rc(
        filename: str,
        dot_rc: str,
        subcommands: Iterable[str],
    ) -> Flags:
        """Returns the flags that should be added to the command line, keyed by
        the subcommand and config for those flags, or the empty tuple if
        they should be applied to all command lines.
        """
        flags: Flags = defaultdict(list)

        with open(dot_rc, 'r') as file:
            line_number = 0
            for line in file.readlines():
                line_number += 1
                line = line.strip()  # Remove leading and trailing whitespaces.

                # Remove any trailing comments.
                index = line.rfind('#')
                if index != -1:
                    line = line[:index]

                if line == '' or line.startswith('#'):
                    continue
                elif re.match(SUBCOMMAND_PATTERN, line):
                    parts = line.split(' ', 1)
                    assert len(parts) == 2
                    flags[(parts[0], None)].extend(shlex.split(parts[1]))
                elif re.match(SUBCOMMAND_CONFIG_PATTERN, line):
                    parts = line.split(' ', 1)
                    assert len(parts) == 2
                    subcommand, config = parts[0].split(':', 1)
                    assert subcommand is not None
                    if subcommand not in [COMMON_PATTERN, *subcommands]:
                        fail(
                            f"'{subcommand}' found at {dot_rc}:{line_number} "
                            "is not a valid subcommand (available subcommands: "
                            f"{', '.join(subcommands)})"
                        )

                    flags[(subcommand, config)].extend(shlex.split(parts[1]))
                else:
                    fail(
                        f"Failed to parse '{filename}' file at {dot_rc}:{line_number}"
                    )

        return flags

    @staticmethod
    def _expand_dot_rc(
        filename: str,
        dot_rc: str,
        parser: argparse.ArgumentParser,
        subcommands: Iterable[str],
        argv: list[str],
    ) -> tuple[list[Flag], list[str], Subcommand]:
        """Expand '.rc' file into `argv`.

        Returns a tuple of (1) expanded flags (vs all flags, which can
        be useful when trying to determine absolute paths of args that
        were expanded from a '.rc' file), and (2) the updated `argv`.
        """
        flags = ArgumentParser._read_flags_from_dot_rc(
            filename, dot_rc, subcommands
        )

        # Now add all "common" flags and parse to determine subcommand.
        common_flags = flags[(COMMON_PATTERN, None)]
        if len(common_flags) > 0:
            argv = argv[:1] + common_flags + argv[1:]

        # Parse command line but only looking for subcommands and
        # '--config=' flags.
        known_args, _ = parser.parse_known_args(args=argv[1:])

        # Expand flags for just '{subcommand}'.
        subcommand = known_args.subcommand

        # Subcommands are required.
        assert subcommand is not None

        subcommand_flags: list[Flag] = []

        # Now add '{subcommand}' specific flags.
        subcommand_flags = flags[(subcommand, None)]
        if len(subcommand_flags) > 0:
            argv.extend(subcommand_flags)

        # Parse the known args again since we might have added some
        # configs from '{subcommand}'.
        known_args, _ = parser.parse_known_args(args=argv[1:])

        assert subcommand == known_args.subcommand

        # Now expand config flags.
        configs = known_args.config or []

        common_config_flags: dict[Config, list[Flag]] = {}
        subcommand_config_flags: dict[Config, list[Flag]] = {}

        while not all(
            (config in common_config_flags) and
            (config in subcommand_config_flags) for config in configs
        ):
            for config in configs:
                # In order for 'config' to be valid we must find
                # either '{COMMON_PATTERN}:{config}' or
                # '{subcommand}:{config}' in the '{filename}' file.
                expanded = (
                    config in common_config_flags and
                    config in subcommand_config_flags
                )

                # Expand '{COMMON_PATTERN}:{config}' flags, but prepend
                # those (after `argv[0]`, but before `argv[1]`).
                if config not in common_config_flags:
                    if (COMMON_PATTERN, config) in flags:
                        expanded = True
                        common_config_flags[config] = flags[
                            (COMMON_PATTERN, config)]
                        argv = argv[:1] + common_config_flags[config] + argv[1:]
                    else:
                        # Store the config so we know it was processed and
                        # we can halt the otherwise infinite while loop.
                        common_config_flags[config] = []

                # Expand '{subcommand}:{config}' flags.
                if config not in subcommand_config_flags:
                    if (subcommand, config) in flags:
                        expanded = True
                        subcommand_config_flags[config] = flags[
                            (subcommand, config)]
                        argv.extend(subcommand_config_flags[config])
                    else:
                        # Store the config so we know it was processed and
                        # we can halt the otherwise infinite while loop.
                        subcommand_config_flags[config] = []

                if not expanded:
                    fail(
                        f"--config={config} is invalid, no "
                        f"'{COMMON_PATTERN}:{config}' nor '{subcommand}:{config}' "
                        f"lines found in {dot_rc}"
                    )

            # Now re-parse the known args so we can see whether or not
            # expanding the last configs added any more configs that
            # we need to continue expanding.
            #
            # NOTE: we pass a copy of `argv` here so that we don't
            # mutate the original `argv` which we'll need to use for
            # our ultimate parsing, after we've expanded all of the
            # configs.
            known_args, _ = parser.parse_known_args(args=argv[1:])

            assert subcommand == known_args.subcommand
            configs = known_args.config

        expanded_flags: list[str] = []

        if (
            len(common_flags) > 0 or len(subcommand_flags) > 0 or
            len(subcommand_config_flags) > 0
        ):
            warn(f"Expanded flags from '{filename}' located at {dot_rc}")
            if len(common_flags) > 0:
                expanded_flags.extend(common_flags)
                warn(
                    f"    {' '.join(common_flags)} (from '{COMMON_PATTERN}' in '{filename}')"
                )

            if len(subcommand_flags) > 0:
                expanded_flags.extend(subcommand_flags)
                warn(
                    f"    {' '.join(subcommand_flags)} (from '{subcommand}' in '{filename}')"
                )

            for config, config_flags in common_config_flags.items():
                if len(config_flags) > 0:
                    expanded_flags.extend(config_flags)
                    warn(
                        f"    {' '.join(config_flags)} (from '{COMMON_PATTERN}:{config}' in '{filename}' via --config={config})"
                    )

            for config, config_flags in subcommand_config_flags.items():
                if len(config_flags) > 0:
                    expanded_flags.extend(config_flags)
                    warn(
                        f"    {' '.join(config_flags)} (from '{subcommand}:{config}' in '{filename}' via --config={config})"
                    )

            # Print a newline here for some extra spacing between any other output or errors.
            print()

        return (expanded_flags, argv, subcommand)
