import json
import sys
from dataclasses import dataclass
from typing import List
from typing import Mapping
from typing import Optional
from typing import Set

import click

from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton.cli import printer
from tecton.cli.command import TectonGroup
from tecton_proto.auth.authorization_service_pb2 import Assignment
from tecton_proto.auth.authorization_service_pb2 import AssignRolesRequest
from tecton_proto.auth.authorization_service_pb2 import GetRolesRequest
from tecton_proto.auth.authorization_service_pb2 import ListAssignedRolesRequest
from tecton_proto.auth.authorization_service_pb2 import UnassignRolesRequest
from tecton_proto.auth.principal_pb2 import PrincipalType
from tecton_proto.auth.resource_pb2 import ResourceType
from tecton_proto.auth.resource_role_assignments_pb2 import RoleAssignmentType
from tecton_proto.metadataservice.metadata_service_pb2 import GetUserRequest


RESOURCE_TYPES = {
    "workspace": ResourceType.RESOURCE_TYPE_WORKSPACE,
    "organization": ResourceType.RESOURCE_TYPE_ORGANIZATION,
}


def _get_role_definitions():
    request = GetRolesRequest()
    response = metadata_service.instance().GetRoles(request)
    return response.roles


@click.command("access-control", cls=TectonGroup)
def access_control():
    """Manage Access Controls"""


@access_control.command("assign-role")
@click.option("-w", "--workspace", required=False)
# we can't make the role help dynamic without making top level usage of the CLI make a network request
# since even lazy loading following https://github.com/pallets/click/pull/2348 doesn't work for help text
@click.option(
    "-r", "--role", required=True, type=str, help="Role name (e.g. admin, owner, editor, consumer, viewer, etc)"
)
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
@click.option("-g", "--principal-group", default=None, help="Principal Group ID")
@click.option("-f", "--file", default=None, help="Newline separated list of user emails.", type=click.File("r"))
def assign_role_command(workspace, role, user, service_account, principal_group, file):
    if file is not None:
        if user or service_account or principal_group:
            msg = "Please use exactly one of: --user, --service-account, --principal-group, or --file"
            raise click.ClickException(msg)
        _bulk_update_user_role(workspace, file, role)
    else:
        """Assign a role to a principal."""
        _update_role(workspace, role, user, service_account, principal_group)


@access_control.command()
@click.option("-w", "--workspace", required=False)
# we can't make the role help dynamic without making top level usage of the CLI make a network request
# since even lazy loading following https://github.com/pallets/click/pull/2348 doesn't work for help text
@click.option(
    "-r", "--role", required=True, type=str, help="Role name (e.g. admin, owner, editor, consumer, viewer, etc)"
)
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
@click.option("-g", "--principal-group", default=None, help="Principal Group ID")
def unassign_role(workspace, role, user, service_account, principal_group):
    """Unassign a role from a principal."""
    _update_role(workspace, role, user, service_account, principal_group, unassign=True)


def _update_role(workspace, role, user, service_account, principal_group, unassign=False):
    role = role.lower()
    assignment = Assignment()
    principal_type, principal_id = get_principal_details(user, service_account, principal_group)

    if workspace:
        if role == "admin":
            msg = "'Admin' is a cluster-wide role. Please remove the --workspace argument."
            raise click.ClickException(msg)
        resource_type = ResourceType.RESOURCE_TYPE_WORKSPACE
        assignment.resource_id = workspace
    else:
        resource_type = ResourceType.RESOURCE_TYPE_ORGANIZATION
    role_defs = _get_role_definitions()
    role_def = next((r for r in role_defs if r.id == role), None)
    if role_def is None:
        msg = f"Invalid role id. Possible values are: {', '.join(r.id for r in role_defs if _is_role_assignable(r, principal_type, resource_type))}"
        raise click.ClickException(msg)

    assignment.resource_type = resource_type
    assignment.principal_type = principal_type
    assignment.principal_id = principal_id
    assignment.role = role_def.legacy_id
    if user is not None:
        human_readable_principal_name = user
    elif service_account is not None:
        human_readable_principal_name = service_account
    else:
        human_readable_principal_name = principal_group
    try:
        if unassign:
            request = UnassignRolesRequest()
            request.assignments.append(assignment)
            metadata_service.instance().UnassignRoles(request)
        else:
            request = AssignRolesRequest()
            request.assignments.append(assignment)
            metadata_service.instance().AssignRoles(request)
        printer.safe_print(f"Successfully updated role for [{human_readable_principal_name}]")
    except Exception as e:
        printer.safe_print(f"Failed to update role for [{human_readable_principal_name}]: {e}", file=sys.stderr)
        sys.exit(1)


def _bulk_update_user_role(workspace, file, role):
    for user in [line.strip() for line in file.readlines() if len(line.strip()) > 0]:
        _update_role(workspace, role, user, service_account=None, principal_group=None)


def _is_role_assignable(role_def, principal_type, resource_type):
    return (
        principal_type in role_def.assignable_to_principal_types
        and resource_type in role_def.assignable_on_resource_types
    )


def get_roles(principal_type, principal_id, resource_type):
    request = ListAssignedRolesRequest()
    request.principal_type = principal_type
    request.principal_id = principal_id
    request.resource_type = resource_type
    response = metadata_service.instance().ListAssignedRoles(request)
    return response


def display_table(headings, ws_roles):
    table = Displayable.from_table(headings=headings, rows=ws_roles, max_width=0)
    # Align columns in the middle horizontally
    table._text_table.set_cols_align(["c" for _ in range(len(headings))])
    printer.safe_print(table)


@dataclass
class ResourceWithRoleAssignments:
    resource_id: Optional[str]

    # sorted list of roles (order will be preserved)
    roles_sorted: List[str]
    # set of roles that have direct assignments
    directly_assigned_roles: Set[str]
    # role to a list of group names that the role is assigned through
    group_assignments_by_role: Mapping[str, List[str]]


@access_control.command("get-roles")
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
@click.option("-g", "--principal-group", default=None, help="Principal Group ID")
@click.option(
    "-r",
    "--resource_type",
    default=None,
    type=click.Choice(RESOURCE_TYPES.keys()),
    help="Optional Resource Type to which the Principal has roles assigned.",
)
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
def get_assigned_roles(user, service_account, principal_group, resource_type, json_out):
    """Get the roles assigned to a principal."""
    if resource_type is not None:
        resource_type = RESOURCE_TYPES[resource_type]
    principal_type, principal_id = get_principal_details(user, service_account, principal_group)

    role_defs = _get_role_definitions()

    ws_roles_response = None
    org_roles_response = None
    try:
        if resource_type is None or resource_type == ResourceType.RESOURCE_TYPE_WORKSPACE:
            ws_roles_response = get_roles(principal_type, principal_id, ResourceType.RESOURCE_TYPE_WORKSPACE)
        if resource_type is None or resource_type == ResourceType.RESOURCE_TYPE_ORGANIZATION:
            org_roles_response = get_roles(principal_type, principal_id, ResourceType.RESOURCE_TYPE_ORGANIZATION)
    except Exception as e:
        printer.safe_print(f"Failed to Get Roles: {e}", file=sys.stderr)
        sys.exit(1)

    ws_roles: List[ResourceWithRoleAssignments] = []
    org_roles = ResourceWithRoleAssignments(None, [], set(), {})

    ws_roles_response = list(ws_roles_response.assignments) if ws_roles_response else []
    org_roles_response = list(org_roles_response.assignments) if org_roles_response else []
    for assignment in ws_roles_response + org_roles_response:
        roles_for_resource: List[str] = []
        roles_assigned_directly: Set[str] = set()
        role_to_group_names: Mapping[str, List[str]] = {}
        for role_granted in assignment.roles_granted:
            role = _maybe_convert_legacy_role_id(role_defs, role_granted.role)
            groups_with_role = []
            for role_source in role_granted.role_assignment_sources:
                if role_source.assignment_type == RoleAssignmentType.ROLE_ASSIGNMENT_TYPE_DIRECT:
                    roles_assigned_directly.add(role)
                elif role_source.assignment_type == RoleAssignmentType.ROLE_ASSIGNMENT_TYPE_FROM_PRINCIPAL_GROUP:
                    group_name = role_source.principal_group_name
                    groups_with_role.append(group_name)
            roles_for_resource.append(role)
            role_to_group_names[role] = groups_with_role

        if len(roles_for_resource) > 0:
            if assignment.resource_type == ResourceType.RESOURCE_TYPE_WORKSPACE:
                ws_roles.append(
                    ResourceWithRoleAssignments(
                        assignment.resource_id,
                        roles_for_resource,
                        roles_assigned_directly,
                        role_to_group_names,
                    )
                )
            elif assignment.resource_type == ResourceType.RESOURCE_TYPE_ORGANIZATION:
                for role in roles_for_resource:
                    if role not in org_roles.roles_sorted:
                        org_roles.roles_sorted.append(role)
                org_roles.directly_assigned_roles.update(roles_assigned_directly)
                org_roles.group_assignments_by_role.update(role_to_group_names)

    # roles are sorted server side, but re-sort in case org roles came from 2 separate calls to getAssignedRoles
    # (workspace roles also return org roles because of roles on all workspaces)
    org_roles.roles_sorted = sorted(org_roles.roles_sorted)

    if json_out:
        json_output = []
        for workspace in ws_roles:
            roles_granted = []
            for role in workspace.roles_sorted:
                assignment_sources = []
                if role in workspace.directly_assigned_roles:
                    assignment_sources.append({"assignment_type": "DIRECT"})
                for group_name in workspace.group_assignments_by_role[role]:
                    assignment_sources.append({"assignment_type": "PRINCIPAL_GROUP", "group_name": group_name})
                roles_granted.append({"role": role, "assignment_sources": assignment_sources})
            json_output.append(
                {"resource_type": "WORKSPACE", "workspace_name": workspace.resource_id, "roles_granted": roles_granted}
            )
        if len(org_roles.roles_sorted) > 0:
            roles_granted = []
            for role in org_roles.roles_sorted:
                assignment_sources = []
                if role in org_roles.directly_assigned_roles:
                    assignment_sources.append({"assignment_type": "DIRECT"})
                for group_name in org_roles.group_assignments_by_role[role]:
                    assignment_sources.append({"assignment_type": "PRINCIPAL_GROUP", "group_name": group_name})
                roles_granted.append({"role": role, "assignment_sources": assignment_sources})
            json_output.append({"resource_type": "ORGANIZATION", "roles_granted": roles_granted})
        printer.safe_print(json.dumps(json_output, indent=4))
    else:
        if len(ws_roles) > 0:
            headings = ["Workspace", "Role", "Assigned Directly", "Assigned via Groups"]
            display_rows = []
            for assignment_for_ws in ws_roles:
                ws_name = assignment_for_ws.resource_id
                already_displayed_ws_name = False
                for role in assignment_for_ws.roles_sorted:
                    ws_name_to_display = "" if already_displayed_ws_name else ws_name
                    already_displayed_ws_name = True
                    assigned_directly = "direct" if role in assignment_for_ws.directly_assigned_roles else ""
                    group_names = ", ".join(assignment_for_ws.group_assignments_by_role[role])
                    ws_role_row = (ws_name_to_display, role, assigned_directly, group_names)

                    display_rows.append(ws_role_row)
            display_table(headings, display_rows)
            printer.safe_print()
        if len(org_roles.roles_sorted) > 0:
            headings = ["Organization Roles", "Assigned Directly", "Assigned via Groups"]
            display_rows = []
            for role in org_roles.roles_sorted:
                assigned_directly = "direct" if role in org_roles.directly_assigned_roles else ""
                group_names = ", ".join(org_roles.group_assignments_by_role[role])
                role_row = (role, assigned_directly, group_names)

                display_rows.append(role_row)
            display_table(headings, display_rows)


def _maybe_convert_legacy_role_id(role_defs, id):
    role_def = next((r for r in role_defs if r.id == id or r.legacy_id == id), None)
    role_id = id if role_def is None else role_def.id
    return role_id


def get_user_id(email):
    try:
        request = GetUserRequest()
        request.email = email
        response = metadata_service.instance().GetUser(request)
        return response.user.okta_id
    except Exception as e:
        printer.safe_print(f"Failed to Get Roles for email [{email}]: {e}", file=sys.stderr)
        sys.exit(1)


def get_principal_details(user, service_account, principal_group):
    principal_type_count = sum([p is not None for p in [user, service_account, principal_group]])
    if principal_type_count > 1:
        msg = "Please mention a single Principal Type using one of --user, --service-account, or --principal-group."
        raise click.ClickException(msg)
    if user:
        return PrincipalType.PRINCIPAL_TYPE_USER, get_user_id(user)
    elif service_account:
        return PrincipalType.PRINCIPAL_TYPE_SERVICE_ACCOUNT, service_account
    elif principal_group:
        return PrincipalType.PRINCIPAL_TYPE_GROUP, principal_group
    else:
        msg = "Please mention a Principal Type using --user, --service-account, or --principal-group."
        raise click.ClickException(msg)
