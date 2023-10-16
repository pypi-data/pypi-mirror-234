import enum
import logging

from tecton._internals import errors
from tecton._internals.metadata_service_impl import auth_lib
from tecton._internals.metadata_service_impl import trace
from tecton_core.errors import FailedPreconditionError
from tecton_core.errors import TectonAPIInaccessibleError
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonNotFoundError


logger = logging.getLogger(__name__)


class gRPCStatus(enum.Enum):
    """gRPC response status codes.

    Status codes are replicated here to avoid importing the `grpc.StatusCode` enum class,
    which requires the grpcio library.

    https://grpc.github.io/grpc/core/md_doc_statuscodes.html
    """

    OK = 0
    CANCELLED = 1
    UNKNOWN = 2
    INVALID_ARGUMENT = 3
    DEADLINE_EXCEEDED = 4
    NOT_FOUND = 5
    ALREADY_EXISTS = 6
    PERMISSION_DENIED = 7
    RESOURCE_EXHAUSTED = 8
    FAILED_PRECONDITION = 9
    ABORTED = 10
    OUT_OF_RANGE = 11
    UNIMPLEMENTED = 12
    INTERNAL = 13
    UNAVAILABLE = 14
    DATA_LOSS = 15
    UNAUTHENTICATED = 16


def raise_for_grpc_status(status_code: int, details: str, host_url: str):
    """
    Raise an exception based on a gRPC error status code.
    """

    if status_code == gRPCStatus.OK.value:
        return

    # Error handling
    if status_code == gRPCStatus.UNAVAILABLE.value:
        raise TectonAPIInaccessibleError(details, host_url)

    if status_code == gRPCStatus.INVALID_ARGUMENT.value:
        raise TectonAPIValidationError(details)

    if status_code == gRPCStatus.FAILED_PRECONDITION.value:
        raise FailedPreconditionError(details)

    if status_code == gRPCStatus.UNAUTHENTICATED.value:
        msg = f"Tecton credentials are invalid, not configured, or expired ({details}). To authenticate using an API key, set TECTON_API_KEY in your environment or use tecton.set_credentials(tecton_api_key=<key>). To authenticate using the CLI, run `tecton login`."
        raise PermissionError(msg)

    if status_code == gRPCStatus.PERMISSION_DENIED.value:
        if not auth_lib.request_has_token():
            # Remove this case in https://tecton.atlassian.net/browse/TEC-9107
            msg = "Tecton credentials have insufficient permissions. To authenticate using an API key, set TECTON_API_KEY in your environment or use tecton.set_credentials(tecton_api_key=<key>). To authenticate using the CLI, run `tecton login`."
            raise PermissionError(msg)
        elif details is not None and "InvalidToken" in details:
            # Remove this case in https://tecton.atlassian.net/browse/TEC-9107
            msg = f"Configured Tecton credentials are not valid ({details})."
            raise PermissionError(msg)
        else:
            msg = f"Insufficient permissions ({details})."
            raise PermissionError(msg)
    if status_code == gRPCStatus.NOT_FOUND.value:
        raise TectonNotFoundError(details)

    logger.debug(f"Unknown MDS exception. code={status_code}, details={details}")

    raise errors.INTERNAL_ERROR_FROM_MDS(details, trace.get_trace_id())
