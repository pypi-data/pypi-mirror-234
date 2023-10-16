import logging

from google.protobuf.empty_pb2 import Empty

from tecton._internals.metadata_service_impl.base_stub import BaseStub
from tecton._internals.metadata_service_impl.http_client import PureHTTPStub
from tecton_core import conf


_stub_instance: BaseStub = None

logger = logging.getLogger(__name__)


def instance() -> BaseStub:
    if not _stub_instance:
        _init_stub_instance()
    return _stub_instance


def close_instance():
    if _stub_instance:
        _stub_instance.close()


def _init_stub_instance():
    global _stub_instance
    _stub_instance = PureHTTPStub()
    conf._init_metadata_server_config(_stub_instance.GetConfigs(Empty()))
