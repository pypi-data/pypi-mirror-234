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

import requests
from google.protobuf import json_format
from yaspin.spinners import Spinners

import tecton
from tecton._internals import metadata_service
from tecton._internals.analytics import StateUpdateEventMetrics
from tecton._internals.analytics import StateUpdateResult
from tecton._internals.utils import plural
from tecton.cli import printer
from tecton.cli.engine_renderer import PlanRenderingClient
from tecton.framework import base_tecton_object
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonNotFoundError
from tecton_core.id_helper import IdHelper
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import repo_metadata_pb2
from tecton_proto.data import state_update_pb2
from tecton_proto.metadataservice import metadata_service_pb2

from .cli_utils import confirm_or_exit
from .error_utils import format_server_errors


def _get_declared_fco_args(
    objects: Sequence[base_tecton_object.BaseTectonObject],
) -> Tuple[List[fco_args_pb2.FcoArgs], repo_metadata_pb2.FeatureRepoSourceInfo]:
    all_args = []
    repo_source_info = repo_metadata_pb2.FeatureRepoSourceInfo()

    for fco_obj in objects:
        all_args.append(fco_obj._build_args())
        repo_source_info.source_info.append(fco_obj._source_info)

    return all_args, repo_source_info


def dump_local_state(objects: base_tecton_object.BaseTectonObject):
    with printer.safe_yaspin(Spinners.earth, text="Collecting local feature declarations") as sp:
        fco_args, repo_source_info = _get_declared_fco_args(objects)
        sp.ok(printer.safe_string("✅"))

    request_plan = metadata_service_pb2.NewStateUpdateRequest(
        request=state_update_pb2.StateUpdateRequest(fco_args=fco_args, repo_source_info=repo_source_info)
    )
    printer.safe_print(json_format.MessageToJson(request_plan, including_default_value_fields=True))


# upload tar.gz of python files to url via PUT request
def _upload_files(repo_files: List[Path], repo_root, url: str):
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
    raise SystemExit(last_error)


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
    no_color: bool = False,
) -> StateUpdateResult:
    # In debug mode we compute the plan synchronously, do not save it in the database, and do not allow to apply it.
    # Primary goal is allowing local development/debugging plans against remote clusters in read-only mode.
    assert not (debug and apply), "Cannot apply in debug mode"
    json_out = json_out_path is not None

    if apply and plan_id:
        # Applying an existing plan, so skip preparing args.
        state_id = IdHelper.from_string(plan_id)
        query_state_update_request = metadata_service_pb2.QueryStateUpdateRequestV2(
            state_id=state_id,
            workspace=workspace_name,
            no_color=no_color,
            json_output=json_out,
            suppress_warnings=suppress_warnings,
        )

        try:
            query_state_update_response = metadata_service.instance().QueryStateUpdateV2(query_state_update_request)
        except (
            TectonInternalError,
            TectonAPIValidationError,
        ) as e:
            printer.safe_print(e)
            return StateUpdateResult.from_error_message(str(e), suppress_recreates)

        if query_state_update_response.error:
            printer.safe_print(query_state_update_response.error)
            return StateUpdateResult.from_error_message(query_state_update_response.error, suppress_recreates)
        if len(query_state_update_response.validation_errors.errors) > 0:
            # Cannot pretty-print validation result using format_server_errors(), because collected local objects
            # might have changed since this plan was generated, so can't accurately match with this plan's FCOs.
            message = "Cannot apply plan because it had errors."
            printer.safe_print(message)
            return StateUpdateResult.from_error_message(message, suppress_recreates)

    else:
        with printer.safe_yaspin(Spinners.earth, text="Collecting local feature declarations") as sp:
            fco_args, repo_source_info = _get_declared_fco_args(objects)
            sp.ok(printer.safe_string("✅"))

        new_state_update_request = metadata_service_pb2.NewStateUpdateRequestV2(
            request=state_update_pb2.StateUpdateRequest(
                workspace=workspace_name,
                upgrade_all=upgrade_all,
                sdk_version=tecton.version.get_semantic_version() or "",
                fco_args=fco_args,
                repo_source_info=repo_source_info,
                suppress_recreates=suppress_recreates,
            ),
            no_color=no_color,
            json_output=json_out,
            suppress_warnings=suppress_warnings,
            blocking_dry_run_mode=debug,
            enable_eager_response=not debug,
        )

        server_side_msg_prefix = "Performing server-side feature validation"
        with printer.safe_yaspin(Spinners.earth, text=f"{server_side_msg_prefix}: Initializing.") as sp:
            try:
                new_state_update_response = metadata_service.instance().NewStateUpdateV2(new_state_update_request)

                if new_state_update_response.HasField("signed_url_for_repo_upload"):
                    _upload_files(repo_files, repo_root, new_state_update_response.signed_url_for_repo_upload)
                if new_state_update_response.HasField("eager_response"):
                    query_state_update_response = new_state_update_response.eager_response
                else:
                    seconds_slept = 0
                    query_state_update_request = metadata_service_pb2.QueryStateUpdateRequestV2(
                        state_id=new_state_update_response.state_id,
                        workspace=workspace_name,
                        no_color=no_color,
                        json_output=json_out,
                        suppress_warnings=suppress_warnings,
                    )
                    while True:
                        query_state_update_response = metadata_service.instance().QueryStateUpdateV2(
                            query_state_update_request
                        )
                        if query_state_update_response.latest_status_message:
                            sp.text = f"{server_side_msg_prefix}: {query_state_update_response.latest_status_message}"
                        if query_state_update_response.ready:
                            break
                        seconds_to_sleep = 5
                        time.sleep(seconds_to_sleep)
                        seconds_slept += seconds_to_sleep
                        if seconds_slept > timeout_seconds:
                            sp.fail(printer.safe_string("⛔"))
                            printer.safe_print("Validation timed out.")
                            return StateUpdateResult.from_error_message("Validation timed out.", suppress_recreates)

                if query_state_update_response.error:
                    sp.fail(printer.safe_string("⛔"))
                    printer.safe_print(query_state_update_response.error)
                    return StateUpdateResult.from_error_message(query_state_update_response.error, suppress_recreates)
                validation_errors = query_state_update_response.validation_errors.errors
                if len(validation_errors) > 0:
                    sp.fail(printer.safe_string("⛔"))
                    format_server_errors(validation_errors, objects, repo_root)
                    return StateUpdateResult.from_error_message(str(validation_errors), suppress_recreates)
                sp.ok(printer.safe_string("✅"))
            except (TectonInternalError, TectonAPIValidationError, TectonNotFoundError) as e:
                sp.fail(printer.safe_string("⛔"))
                printer.safe_print(e)
                return StateUpdateResult.from_error_message(str(e), suppress_recreates)

        state_id = new_state_update_response.state_id

    plan_rendering_client = PlanRenderingClient(query_state_update_response)

    if not plan_rendering_client.has_diffs():
        plan_rendering_client.print_empty_plan()
    else:
        plan_rendering_client.print_plan()

        if apply:
            plan_rendering_client.print_apply_warnings()
            if interactive:
                confirm_or_exit(f'Are you sure you want to apply this plan to: "{workspace_name}"?')

            apply_request = metadata_service_pb2.ApplyStateUpdateRequest(state_id=state_id)
            metadata_service.instance().ApplyStateUpdate(apply_request)

            num_fcos = plan_rendering_client.num_fcos_changed
            printer.safe_print(
                f'🎉 Done! Applied changes to {num_fcos} {plural(num_fcos, "object", "objects")} in workspace "{workspace_name}".'
            )

    if json_out_path:
        repo_diff_summary = plan_rendering_client.get_json_plan_output()
        json_out_path.parent.mkdir(parents=True, exist_ok=True)
        json_out_path.write_text(repo_diff_summary)

    return StateUpdateResult(
        state_update_event_metrics=StateUpdateEventMetrics(
            num_total_fcos=len(objects),
            suppress_recreates=suppress_recreates,
            json_out=(json_out_path is not None),
            error_message=None,
            num_fcos_changed=query_state_update_response.successful_plan_output.num_fcos_changed,
            num_warnings=query_state_update_response.successful_plan_output.num_warnings,
        ),
        success_response=query_state_update_response,
    )
