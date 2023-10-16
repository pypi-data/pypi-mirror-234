import os
import sys
import tempfile
from datetime import datetime
from datetime import timezone
from typing import Optional

import click
from google.protobuf import timestamp_pb2

from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.cli_utils import display_table
from tecton.cli.command import TectonGroup
from tecton.cli.dependency_resolver import resolve_dependencies
from tecton_proto.common.container_image_pb2 import ContainerImage
from tecton_proto.data.remote_compute_environment_pb2 import RemoteEnvironmentStatus
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import CreateRemoteEnvironmentRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import DeleteRemoteEnvironmentsRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import ListRemoteEnvironmentsRequest


DEFAULT_PYTHON_VERSION = "3.8"
RESOLVED_REQUIREMENTS_FILENAME = "resolved_requirements.txt"
ERROR_MESSAGE_PREFIX = "⛔ ERROR: "
DEPENDENCY_RESOLUTION_TIMEOUT_SECONDS = 60


@click.command("environment", cls=TectonGroup)
def environment():
    """Manage Environments for ODFV Execution"""


@environment.command("list-all")
def list_all():
    """List all available Python Environments"""
    remote_environments = _list_environments()
    _display_environments(remote_environments)


@environment.command("list")
@click.option("--id", help="Environment Id", required=False, type=str)
@click.option("--name", help="Environment Name", required=False, type=str)
def list(id: Optional[str] = None, name: Optional[str] = None):
    """List Python Environment(s) matching a name or an ID"""
    if not id and not name:
        remote_environments = _list_environments()
        _display_environments(remote_environments)
    else:
        identifier = name if name is not None else id
        by_name = name is not None
        remote_environments = _list_environments(identifier=identifier, by_name=by_name)
        _display_environments(remote_environments)


@environment.command("create")
@click.option("-n", "--name", help="Environment name", required=True, type=str)
@click.option("-d", "--description", help="Environment description", required=True, type=str)
@click.option(
    "-r", "--requirements", help="Path to requirements.txt file", required=False, type=click.Path(exists=True)
)
@click.option("-p", "--python-version", help="Python Version for the environment")
@click.option(
    "-i", "--image-uri", help="Image URI. This functionality is in Private Preview.", required=False, type=str
)
def create(
    name: str,
    description: str,
    requirements: Optional[str] = None,
    python_version: Optional[str] = None,
    image_uri: Optional[str] = None,
):
    """Create a custom Python Environment
    Parameters:
       name (str): The name of the environment.
       description (str): The description of the environment.
       requirements (str, optional): The path to the requirements.txt file containing all dependencies for the environment
       python_version (str, optional): The Python version to use, defaults to "3.8"
       image_uri (str, optional): The URI of the image to use for the environment. This functionality is in Private Preview.
    """
    if image_uri is not None and requirements is not None:
        printer.safe_print(
            f"{ERROR_MESSAGE_PREFIX} Exactly one of parameters `requirements` and `image_uri` must be specified.",
            file=sys.stderr,
        )
        sys.exit(1)
    if image_uri is not None:
        resp = _create_environment_with_image(name, description, image_uri)
        _display_environments([resp.remote_environment])
    elif requirements is not None:
        _python_version = python_version or DEFAULT_PYTHON_VERSION
        _create_environment_with_requirements(name, description, requirements, _python_version)
    else:
        printer.safe_print(
            f"{ERROR_MESSAGE_PREFIX} Please specify the path to a `requirements.txt` file via the `requirements` parameter to create an environment",
            file=sys.stderr,
        )
        sys.exit(1)


# Enable environment deletion in 0.8
'''
@environment.command("delete")
@click.option("--id", help="Environment ID", required=False, type=str)
@click.option("--name", help="Environment Name", required=False, type=str)
def delete(id: Optional[str] = None, name: Optional[str] = None):
    """Delete an existing custom Python Environment by name or an ID"""
    if id is None and name is None:
        printer.safe_print("At least one of `id` or `name` must be provided", file=sys.stderr)
        sys.exit(1)

    identifier = name if name is not None else id
    by_name = name is not None
    environments = _list_environments(identifier=identifier, by_name=by_name)
    if not environments:
        printer.safe_print(
            f"No matching environments found for: {identifier}. Please verify available environments using the `list_all` command",  file=sys.stderr
        )
    elif len(environments) > 1:
        printer.safe_print(
            f"No matching environment found for: {identifier}. Did you mean one of the following environment(s)? \n\n", file=sys.stderr
        )
        _display_environments(environments)
    else:
        environment_to_delete = environments[0]
        confirmation_text = f"Are you sure you want to delete environment {environment_to_delete.name}? (y/n) :"
        confirmation = input(confirmation_text).lower().strip()
        if confirmation == "y":
            try:
                _delete_environment(env_id=environment_to_delete.id)
                printer.safe_print(f"Successfully deleted environment: {identifier}")
            except Exception as e:
                printer.safe_print(f"Failed to delete. error = {str(e)}, type= {type(e).__name__}")
        else:
            printer.safe_print(f"Cancelled deletion for environment: {identifier}")
'''


def _display_environments(environments: list):
    headings = ["Id", "Name", "Status", "Created At", "Updated At"]
    display_table(
        headings,
        [
            (
                i.id,
                i.name,
                RemoteEnvironmentStatus.Name(i.status),
                _timestamp_to_string(i.created_at),
                _timestamp_to_string(i.updated_at),
            )
            for i in environments
        ],
    )


def _create_environment_with_image(name: str, description: str, image_uri):
    try:
        req = CreateRemoteEnvironmentRequest()
        req.name = name
        req.description = description

        image_info = ContainerImage()
        image_info.image_uri = image_uri

        req.image_info.CopyFrom(image_info)

        return metadata_service.instance().CreateRemoteEnvironment(req)
    except PermissionError as e:
        printer.safe_print(
            "The user is not authorized to create environment(s) in Tecton. Please reach out to your Admin to complete this "
            "action",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        printer.safe_print(f"Failed to create environment: {e}", file=sys.stderr)
        sys.exit(1)


def _create_environment_with_requirements(name: str, description: str, requirements_path: str, python_version: str):
    """Create a custom environment by resolving dependencies, downloading wheels and updating MDS
    Parameters:
        name(str): Name of the custom environment
        description(str): Description of the custom environment
        requirements_path(str): Path to the `requirements.txt` file
        python_version(str): The Python version to resolve the dependencies for
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        printer.safe_print("\n⏳ Resolving Dependencies. This may take a few seconds.....")
        resolved_requirements_path = os.path.join(tmpdir, RESOLVED_REQUIREMENTS_FILENAME)
        try:
            resolve_dependencies(
                python_version=python_version,
                requirements_path=requirements_path,
                resolved_requirements_path=resolved_requirements_path,
                timeout_seconds=DEPENDENCY_RESOLUTION_TIMEOUT_SECONDS,
            )
        except ValueError as e:
            printer.safe_print(f"{ERROR_MESSAGE_PREFIX} {e}", file=sys.stderr)
            sys.exit(1)
        printer.safe_print("✅ Successfully resolved dependencies")
        # TODO(Pooja) Do rest of environment creation below


def _delete_environment(env_id: str):
    try:
        req = DeleteRemoteEnvironmentsRequest()
        req.ids.append(env_id)
        return metadata_service.instance().DeleteRemoteEnvironments(req)
    except PermissionError as e:
        printer.safe_print(
            "The user is not authorized to perform environment deletion. Please reach out to your Admin to complete this action",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        printer.safe_print(f"Failed to delete environment: {e}", file=sys.stderr)
        sys.exit(1)


def _list_environments(identifier: Optional[str] = None, by_name: bool = False):
    try:
        req = ListRemoteEnvironmentsRequest()
        response = metadata_service.instance().ListRemoteEnvironments(req)

        if identifier is None:
            return response.remote_environments

        if by_name:
            environments = [env for env in response.remote_environments if identifier in env.name]
            error_message = f"Unable to find environments with name: {identifier}"
        else:
            environments = [env for env in response.remote_environments if identifier in env.id]
            error_message = f"Unable to find environment with id: {identifier}"

        if len(environments) < 1:
            printer.safe_print(error_message, file=sys.stderr)
            sys.exit(1)

        return environments

    except Exception as e:
        printer.safe_print(f"Failed to fetch environments: {e}", file=sys.stderr)
        sys.exit(1)


def _timestamp_to_string(value: timestamp_pb2.Timestamp) -> str:
    t = datetime.fromtimestamp(value.ToSeconds())
    return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
