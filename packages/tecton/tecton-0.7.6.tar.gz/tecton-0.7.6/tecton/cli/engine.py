import io
import os
import sys
import tarfile
import time
from pathlib import Path
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import requests
from google.protobuf.json_format import MessageToJson
from yaspin.spinners import Spinners

import tecton
from tecton._internals import metadata_service
from tecton._internals.analytics import StateUpdateEventMetrics
from tecton._internals.analytics import StateUpdateResponse
from tecton._internals.utils import is_live_workspace
from tecton.cli import printer
from tecton.cli.engine_renderer import ThickPlanRenderingClient
from tecton.cli.engine_renderer import ThinPlanRenderingClient
from tecton.framework import base_tecton_object
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonInternalError
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.id_helper import IdHelper
from tecton_proto.args.fco_args_pb2 import FcoArgs
from tecton_proto.args.repo_metadata_pb2 import FeatureRepoSourceInfo
from tecton_proto.data.state_update_pb2 import StateUpdateRequest
from tecton_proto.data.state_update_pb2 import ValidationMessage
from tecton_proto.metadataservice.metadata_service_pb2 import ApplyStateUpdateRequest
from tecton_proto.metadataservice.metadata_service_pb2 import NewStateUpdateRequest
from tecton_proto.metadataservice.metadata_service_pb2 import NewStateUpdateRequestV2
from tecton_proto.metadataservice.metadata_service_pb2 import QueryStateUpdateRequest
from tecton_proto.metadataservice.metadata_service_pb2 import QueryStateUpdateRequestV2
from tecton_proto.metadataservice.metadata_service_pb2 import QueryStateUpdateResponse
from tecton_proto.metadataservice.metadata_service_pb2 import QueryStateUpdateResponseV2

from .cli_utils import confirm_or_exit
from .error_utils import format_server_errors


def get_declared_fco_args(
    objects: Sequence[base_tecton_object.BaseTectonObject],
) -> Tuple[List[FcoArgs], FeatureRepoSourceInfo]:
    all_args = []
    repo_source_info = FeatureRepoSourceInfo()

    for fco_obj in objects:
        all_args.append(fco_obj._build_args())
        repo_source_info.source_info.append(fco_obj._source_info)

    return all_args, repo_source_info


def dump_local_state(objects: base_tecton_object.BaseTectonObject):
    with printer.safe_yaspin(Spinners.earth, text="Collecting local feature declarations") as sp:
        fco_args, repo_source_info = get_declared_fco_args(objects)
        sp.ok(printer.safe_string("✅"))

    request_plan = NewStateUpdateRequest(
        request=StateUpdateRequest(fco_args=fco_args, repo_source_info=repo_source_info)
    )
    printer.safe_print(MessageToJson(request_plan, including_default_value_fields=True))


# upload tar.gz of python files to url via PUT request
def upload_files(repo_files: List[Path], repo_root, url: str):
    tar_bytes = io.BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode="w|gz") as targz:
        for f in repo_files:
            targz.add(f, arcname=os.path.relpath(f, repo_root))
    for _ in range(3):
        try:
            r = requests.put(url, data=tar_bytes.getbuffer())
            if r.status_code != 200:
                # We will get 403 (forbidden) when the signed url expires.
                if r.status_code == 403:
                    printer.safe_print(
                        "\nUploading feature repo failed due to expired session. Please retry the command."
                    )
                else:
                    printer.safe_print(f"\nUploading feature repo failed with reason: {r.reason}")
                sys.exit(1)
            return
        except requests.RequestException as e:
            last_error = e
    else:
        raise SystemExit(last_error)


def _construct_new_plan_request_v1(
    workspace_name: str,
    upgrade_all: bool,
    fco_args: List[FcoArgs],
    repo_source_info: FeatureRepoSourceInfo,
    suppress_recreates: bool,
    debug: bool,
) -> NewStateUpdateRequest:
    request_plan = NewStateUpdateRequest()
    request_plan.request.workspace = workspace_name

    request_plan.request.upgrade_all = upgrade_all
    request_plan.request.sdk_version = tecton.version.get_semantic_version() or ""

    request_plan.request.fco_args.extend(fco_args)
    request_plan.request.repo_source_info.CopyFrom(repo_source_info)
    request_plan.request.suppress_recreates = suppress_recreates

    if debug:
        request_plan.blocking_dry_run_mode = True
    else:
        request_plan.enable_eager_response = True

    return request_plan


def _construct_new_plan_request_v2_from_v1(
    request_v1: NewStateUpdateRequest,
    no_color: bool,
    json_out: bool,
) -> NewStateUpdateRequestV2:
    request_plan = NewStateUpdateRequestV2()
    request_plan.request.CopyFrom(request_v1.request)
    request_plan.blocking_dry_run_mode = request_v1.blocking_dry_run_mode
    request_plan.enable_eager_response = request_v1.enable_eager_response
    request_plan.no_color = no_color
    request_plan.json_output = json_out

    return request_plan


def _construct_query_plan_request_v2_from_v1(
    request_v1: QueryStateUpdateRequest,
    no_color: bool,
    json_out: bool,
) -> QueryStateUpdateRequestV2:
    query_request = QueryStateUpdateRequestV2()
    query_request.state_id.CopyFrom(request_v1.state_id)
    query_request.workspace = request_v1.workspace
    query_request.no_color = no_color
    query_request.json_output = json_out

    return query_request


def _execute_new_state_update_v1_or_v2(
    request_v1: NewStateUpdateRequest,
    enable_server_side_rendering: bool,
    no_color: bool,
    json_out: bool,
):
    if enable_server_side_rendering:
        request_v2 = _construct_new_plan_request_v2_from_v1(request_v1, no_color, json_out)
        return metadata_service.instance().NewStateUpdateV2(request_v2)
    else:
        return metadata_service.instance().NewStateUpdate(request_v1)


def _execute_query_state_update_v1_or_v2(
    request_v1: QueryStateUpdateRequest,
    enable_server_side_rendering: bool,
    no_color: bool,
    json_out: bool,
):
    if enable_server_side_rendering:
        request_v2 = _construct_query_plan_request_v2_from_v1(request_v1, no_color, json_out)
        return metadata_service.instance().QueryStateUpdateV2(request_v2)
    else:
        return metadata_service.instance().QueryStateUpdate(request_v1)


def _get_validation_errors(
    query_response: Union[QueryStateUpdateResponse, QueryStateUpdateResponseV2], enable_server_side_rendering: bool
) -> List[ValidationMessage]:
    if enable_server_side_rendering:
        if query_response.validation_errors.errors:
            return query_response.validation_errors.errors
    else:
        if query_response.validation_result.errors:
            return query_response.validation_result.errors
    return []


def update_tecton_state(
    objects: List[base_tecton_object.BaseTectonObject],
    repo_files: List[Path],
    repo_root: Optional[str],
    apply,
    debug,
    interactive,
    upgrade_all: bool,
    workspace_name: str,
    suppress_warnings: bool = False,
    suppress_recreates: bool = False,
    json_out_path: Optional[Path] = None,
    timeout_seconds=90 * 60,
    plan_id: Optional[str] = None,
    no_color: bool = False,  # used for plan rendering on server-side
    enable_server_side_rendering: bool = True,
) -> StateUpdateResponse:
    # In debug mode we compute the plan synchronously, do not save it in the database, and do not allow to apply it.
    # Primary goal is allowing local development/debugging plans against remote clusters in read-only mode.
    assert not (debug and apply), "Cannot apply in debug mode"
    json_out = json_out_path is not None

    if apply and plan_id:
        # Applying an existing plan, so skip preparing args.
        state_id = IdHelper.from_string(plan_id)
        request_query = QueryStateUpdateRequest()
        request_query.state_id.CopyFrom(state_id)
        request_query.workspace = workspace_name

        try:
            response_query = _execute_query_state_update_v1_or_v2(
                request_query,
                enable_server_side_rendering,
                no_color,
                json_out,
            )
        except (
            TectonInternalError,
            TectonAPIValidationError,
        ) as e:
            printer.safe_print(e)
            return StateUpdateResponse.from_error_message(str(e), suppress_recreates)

        if response_query.error:
            printer.safe_print(response_query.error)
            return StateUpdateResponse.from_error_message(response_query.error, suppress_recreates)
        if len(_get_validation_errors(response_query, enable_server_side_rendering)) > 0:
            # Cannot pretty-print validation result using format_server_errors(), because collected local objects
            # might have changed since this plan was generated, so can't accurately match with this plan's FCOs.
            message = "Cannot apply plan because it had errors."
            printer.safe_print(message)
            return StateUpdateResponse.from_error_message(message, suppress_recreates)

    else:
        with printer.safe_yaspin(Spinners.earth, text="Collecting local feature declarations") as sp:
            fco_args, repo_source_info = get_declared_fco_args(objects)
            sp.ok(printer.safe_string("✅"))

        new_plan_request = _construct_new_plan_request_v1(
            workspace_name, upgrade_all, fco_args, repo_source_info, suppress_recreates, debug
        )

        server_side_msg_prefix = "Performing server-side feature validation"
        with printer.safe_yaspin(Spinners.earth, text=f"{server_side_msg_prefix}: Initializing.") as sp:
            try:
                new_plan_response = _execute_new_state_update_v1_or_v2(
                    new_plan_request,
                    enable_server_side_rendering,
                    no_color,
                    json_out,
                )

                if new_plan_response.HasField("signed_url_for_repo_upload"):
                    upload_files(repo_files, repo_root, new_plan_response.signed_url_for_repo_upload)
                if new_plan_response.HasField("eager_response"):
                    response_query = new_plan_response.eager_response
                else:
                    seconds_slept = 0
                    request_query = QueryStateUpdateRequest()
                    request_query.workspace = workspace_name
                    request_query.state_id.CopyFrom(new_plan_response.state_id)
                    while True:
                        response_query = _execute_query_state_update_v1_or_v2(
                            request_query,
                            enable_server_side_rendering,
                            no_color,
                            json_out,
                        )
                        if response_query.latest_status_message:
                            sp.text = f"{server_side_msg_prefix}: {response_query.latest_status_message}"
                        if response_query.ready:
                            break
                        seconds_to_sleep = 5
                        time.sleep(seconds_to_sleep)
                        seconds_slept += seconds_to_sleep
                        if seconds_slept > timeout_seconds:
                            sp.fail(printer.safe_string("⛔"))
                            printer.safe_print("Validation timed out.")
                            return StateUpdateResponse.from_error_message("Validation timed out.", suppress_recreates)

                if response_query.error:
                    sp.fail(printer.safe_string("⛔"))
                    printer.safe_print(response_query.error)
                    return StateUpdateResponse.from_error_message(response_query.error, suppress_recreates)
                validation_errors = _get_validation_errors(response_query, enable_server_side_rendering)
                if len(validation_errors) > 0:
                    sp.fail(printer.safe_string("⛔"))
                    format_server_errors(validation_errors, objects, repo_root)
                    return StateUpdateResponse.from_error_message(str(validation_errors), suppress_recreates)
                sp.ok(printer.safe_string("✅"))
            except (
                TectonInternalError,
                TectonAPIValidationError,
            ) as e:
                sp.fail(printer.safe_string("⛔"))
                printer.safe_print(e)
                return StateUpdateResponse.from_error_message(str(e), suppress_recreates)

        state_id = new_plan_response.state_id

    if enable_server_side_rendering:
        plan_rendering_client = ThinPlanRenderingClient(response_query)
    else:
        plan_rendering_client = ThickPlanRenderingClient(
            response_query.diff_items,
            response_query.validation_result.warnings,
            state_id,
            suppress_warnings,
            workspace_name,
            is_live_workspace(workspace_name),
            debug,
            response_query.recreates_suppressed,
        )

    if not plan_rendering_client.has_diffs():
        plan_rendering_client.print_empty_plan()
    else:
        plan_rendering_client.print_plan()

        if apply:
            plan_rendering_client.print_apply_warnings()
            if interactive:
                confirm_or_exit(f'Are you sure you want to apply this plan to: "{workspace_name}"?')

            request_apply = ApplyStateUpdateRequest()
            request_apply.state_id.CopyFrom(state_id)
            metadata_service.instance().ApplyStateUpdate(request_apply)

            printer.safe_print("🎉 all done!")

    if json_out_path:
        repo_diff_summary = plan_rendering_client.get_json_plan_output()
        json_out_path.parent.mkdir(parents=True, exist_ok=True)
        json_out_path.write_text(repo_diff_summary)

    num_v3_fcos = sum(
        obj._args.version in (FrameworkVersion.UNSPECIFIED.value, FrameworkVersion.FWV3.value) for obj in objects
    )
    num_v5_fcos = sum(obj._args.version is FrameworkVersion.FWV5.value for obj in objects)

    v1_response = None
    v2_response = None
    if enable_server_side_rendering:
        v2_response = response_query
    else:
        v1_response = response_query

    return StateUpdateResponse(
        state_update_event_metrics=StateUpdateEventMetrics(
            num_total_fcos=len(objects),
            num_fcos_changed=plan_rendering_client.num_fcos_changed,
            num_v3_fcos=num_v3_fcos,
            num_v5_fcos=num_v5_fcos,
            suppress_recreates=suppress_recreates,
            json_out=(json_out_path is not None),
            num_warnings=plan_rendering_client.num_warnings,
        ),
        v1_response=v1_response,
        v2_response=v2_response,
    )
