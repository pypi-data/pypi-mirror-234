import json
import sys

import click

from .cli_utils import pprint_dict
from .cli_utils import print_version_msg
from tecton.cli import printer
from tecton.cli.command import TectonGroup
from tecton.identities import api_keys
from tecton_core.errors import TectonAPIValidationError
from tecton_core.id_helper import IdHelper


# TODO(fix the "readonly" part of this help string)
@click.command("api-key", cls=TectonGroup)
def api_key():
    """Interact with Tecton read-only API keys."""


@api_key.command()
@click.option("--description", default="", help="An optional, human readable description for this API key.")
@click.option(
    "--is-admin",
    is_flag=True,
    default=False,
    help="Whether the API key has admin permissions, generally corresponding to write permissions. Defaults to false.",
)
def create(description, is_admin):
    """[DEPRECATED] Create a new API key. Use `tecton service-account create` instead."""
    print_version_msg(
        "Warning: `tecton api-key create` is deprecated and will be removed in 0.7. To create a service account, use `tecton service-account create`. To assign the Admin role to the service account, use `tecton access-control assign-role -r admin -s <service-account-id>`.",
    )
    response = api_keys.create(description, is_admin)
    printer.safe_print("Save this key - you will not be able to get it again.", file=sys.stderr)
    printer.safe_print(response.key)


def introspect(api_key):
    response = api_keys.introspect(api_key)
    if not response:
        printer.safe_print(
            f"API key cannot be found. Ensure you have the correct API Key. The key's secret value is different from the key's ID.",
            file=sys.stderr,
        )
        sys.exit(1)
    return {
        "API Key ID": IdHelper.to_string(response.id),
        "Description": response.description,
        "Created by": response.created_by,
        "Active": response.active,
    }


@api_key.command("introspect")
@click.argument("api-key", required=True)
@click.option(
    "--json-output",
    is_flag=True,
    default=False,
    help="Whether the output is displayed in machine readable json format. Defaults to false.",
)
def introspect_command(api_key, json_output):
    """Introspect an API Key"""
    api_key_details = introspect(api_key)
    if json_output:
        for key in api_key_details.copy():
            snake_case = key.replace(" ", "_").lower()
            api_key_details[snake_case] = api_key_details.pop(key)
        printer.safe_print(f"{json.dumps(api_key_details)}")
    else:
        pprint_dict(api_key_details, colwidth=16)


@api_key.command()
@click.argument("id", required=True)
def delete(id):
    """[DEPRECATED] Deactivate an API key by its ID. Use `tecton service-account deactivate` and `tecton service-account delete` instead."""
    print_version_msg(
        "Warning: `tecton api-key delete` is deprecated and will be removed in 0.7. To deactivate or delete a service account, use `tecton service-account deactivate` or `tecton service-account delete`.",
    )
    try:
        response = api_keys.delete(id)
    except TectonAPIValidationError as e:
        printer.safe_print(
            f"API key with ID {id} not found. Check `tecton api-key list` to find the IDs of currently active API keys. The key's ID is different from the key's secret value."
        )
        sys.exit(1)
    printer.safe_print("Success")


@api_key.command()
def list():
    """[DEPRECATED] List active API keys. Use `tecton service-account list` instead."""
    print_version_msg(
        "Warning: `tecton api-key list` is deprecated and will be removed in 0.7. To list all service accounts, use `tecton service-account list`.",
    )
    response = api_keys.list()
    for k in response.api_keys:
        printer.safe_print(f"API Key ID: {IdHelper.to_string(k.id)}")
        printer.safe_print(f"Secret Key: {k.obscured_key}")
        printer.safe_print(f"Description: {k.description}")
        printer.safe_print(f"Created by: {k.created_by}")
        printer.safe_print()
