from google.protobuf.descriptor import ServiceDescriptor
from google.protobuf.descriptor_pb2 import MethodOptions
from resemble.v1alpha1 import options_pb2


def get_method_options(options: MethodOptions) -> options_pb2.MethodOptions:
    """Takes a proto descriptor of options specified on a method, and extracts
    the resemble.MethodOptions, if such an option is set.
    """
    # This is the proto API for accessing our custom options used in the
    # given `MethodOptions`. Returns an empty resemble.MethodOptions if no
    # option is set, which means its options will default to the proto
    # defaults for their field types.
    return options.Extensions[options_pb2.method]


def is_resemble_service(service: ServiceDescriptor) -> bool:
    """Check if the service is a Resemble service.

    A resemble service MUST have ServiceOptions annotation.
    """
    has_service_annotation = False

    for _, value in service.GetOptions().ListFields():
        if isinstance(value, options_pb2.ServiceOptions):
            has_service_annotation = True

    for method in service.methods:
        is_resemble_method = False
        for _, value in method.GetOptions().ListFields():
            if isinstance(value, options_pb2.MethodOptions):
                is_resemble_method = True
        if has_service_annotation and not is_resemble_method:
            raise ValueError(
                f"Missing resemble method annotation for '{service.full_name}.{method.name}'"
            )
        elif not has_service_annotation and is_resemble_method:
            raise ValueError(
                "Found resemble method annotations in "
                f"'{service.full_name}.{method.name}', but '{service.full_name}' is "
                "not a resemble service. (Did you forget to add the resemble "
                f"state annotation to '{service.full_name}'?)"
            )

    return has_service_annotation
