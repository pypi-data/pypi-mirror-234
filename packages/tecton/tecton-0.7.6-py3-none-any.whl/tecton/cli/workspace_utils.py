import sys

from tecton._internals import metadata_service
from tecton.cli import printer
from tecton_proto.metadataservice.metadata_service_pb2 import ListWorkspacesRequest


def check_workspace_exists(workspace_name: str):
    workspace_names = {w.name for w in _list_workspaces()}
    if workspace_name not in workspace_names:
        printer.safe_print(
            f'Workspace "{workspace_name}" not found. Run `tecton workspace list` to see list of available workspaces.'
        )
        sys.exit(1)


def _list_workspaces():
    request = ListWorkspacesRequest()
    response = metadata_service.instance().ListWorkspaces(request)
    return response.workspaces
