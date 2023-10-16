import sys

import click

from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton.cli import printer
from tecton.cli.command import TectonGroup
from tecton_proto.common.container_image_pb2 import ContainerImage
from tecton_proto.data.remote_compute_environment_pb2 import RemoteEnvironmentStatus
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import CreateRemoteEnvironmentRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import DeleteRemoteEnvironmentsRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import ListRemoteEnvironmentsRequest


@click.command("environment", cls=TectonGroup)
def environment():
    """Manage Environments for ODFV Execution"""


@environment.command("list-all")
def list_all():
    """List all available Python Environments"""
    response = _list_environments()
    headings = ["Id", "Name", "Status"]
    display_table(
        headings,
        [(i.id, i.name, RemoteEnvironmentStatus.Name(i.status)) for i in response.remote_environments],
    )


@environment.command("create")
@click.option("-n", "--name", help="Environment name", required=True, type=str)
@click.option("-d", "--description", help="Environment description", required=True, type=str)
@click.option("-i", "--image-uri", help="Image URI", required=True, type=str)
def create(name: str, description: str, image_uri: str):
    resp = _create_environment(name, description, image_uri)
    headings = ["Id", "Name", "Status", "Image"]
    env = resp.remote_environment
    display_table(headings, [(env.id, env.name, RemoteEnvironmentStatus.Name(env.status), env.image_info.image_uri)])


@environment.command("delete")
@click.option("--id", help="Environment ID", required=True, type=str)
def delete(id: str):
    _delete_environment(id)
    printer.safe_print(f"Successfully deleted environment: {id}")


def display_table(headings, ws_roles):
    table = Displayable.from_table(headings=headings, rows=ws_roles, max_width=0)
    # Align columns in the middle horizontally
    table._text_table.set_cols_align(["c" for _ in range(len(headings))])
    printer.safe_print(table)


def _create_environment(name: str, description: str, image_uri):
    try:
        req = CreateRemoteEnvironmentRequest()
        req.name = name
        req.description = description

        image_info = ContainerImage()
        image_info.image_uri = image_uri

        req.image_info.CopyFrom(image_info)

        return metadata_service.instance().CreateRemoteEnvironment(req)
    except Exception as e:
        printer.safe_print(f"Failed to create environment: {e}", file=sys.stderr)
        sys.exit(1)


def _delete_environment(env_id: str):
    try:
        req = DeleteRemoteEnvironmentsRequest()
        req.ids.append(env_id)
        return metadata_service.instance().DeleteRemoteEnvironments(req)
    except Exception as e:
        printer.safe_print(f"Failed to create environment: {e}", file=sys.stderr)
        sys.exit(1)


def _list_environments():
    try:
        req = ListRemoteEnvironmentsRequest()
        return metadata_service.instance().ListRemoteEnvironments(req)
    except Exception as e:
        printer.safe_print(f"Failed to list all environments: {e}", file=sys.stderr)
        sys.exit(1)
