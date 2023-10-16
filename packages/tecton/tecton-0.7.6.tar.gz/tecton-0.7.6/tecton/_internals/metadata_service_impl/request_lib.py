import urllib.parse
from typing import Dict

from tecton import version
from tecton._internals.metadata_service_impl import auth_lib
from tecton._internals.metadata_service_impl.trace import get_trace_id
from tecton_core import conf
from tecton_core import errors
from tecton_core.id_helper import IdHelper


def request_headers() -> Dict[str, str]:
    """
    :return: Dictionary of request metadata.
    """
    metadata = {}

    metadata["x-request-id"] = IdHelper.generate_string_id()
    trace_id = get_trace_id()
    if trace_id:
        metadata["x-trace-id"] = trace_id

    # when running from dev environment, package version might not be set
    _version = version.get_semantic_version()
    if _version:
        metadata["x-tecton-client-version"] = _version

    workspace = conf.get_or_none("TECTON_WORKSPACE")
    if workspace:
        metadata["x-workspace"] = workspace
        # Warning: This is a hack to make it possible to integration test both EMR and Databricks
        # in a single deployment.
        if workspace.endswith("__emr"):
            metadata["x-tecton-force-emr"] = "true"

    authorization = auth_lib.get_auth_header()
    if authorization:
        metadata["authorization"] = authorization

    parsed_url = urllib.parse.urlparse(request_url())
    metadata["host"] = parsed_url.netloc

    return metadata


def request_url() -> str:
    """
    :return: A Validated API service URL.
    """
    api_service = conf.get_or_none("API_SERVICE")
    if not api_service:
        msg = "API_SERVICE not set. Please configure API_SERVICE or use tecton.set_credentials(tecton_url=<url>)"
        raise errors.TectonAPIValidationError(msg)
    conf.validate_api_service_url(api_service)
    return urllib.parse.urljoin(api_service + "/", "proxy")
