import io
import os
import sys
import tarfile
import time
from pathlib import Path
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

import requests
from colorama import Fore
from colorama import Style
from google.protobuf.json_format import MessageToJson
from yaspin.spinners import Spinners

import tecton
from .cli_utils import code_diff
from .cli_utils import confirm_or_exit
from .cli_utils import human_fco_type
from .error_utils import format_server_errors
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals.analytics import TectonStateUpdateMetrics
from tecton._internals.feature_definition import FeatureDefinition
from tecton._internals.utils import is_live_workspace
from tecton.cli import printer
from tecton.cli.command import _cluster_url
from tecton.declarative import FeatureService
from tecton.declarative.base import BaseDataSource
from tecton.declarative.entity import Entity
from tecton.declarative.transformation import Transformation
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonInternalError
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.id_helper import IdHelper
from tecton_proto.args.diff_options_pb2 import FcoPropertyRenderingType
from tecton_proto.args.entity_pb2 import EntityArgs
from tecton_proto.args.fco_args_pb2 import FcoArgs
from tecton_proto.args.feature_service_pb2 import FeatureServiceArgs
from tecton_proto.args.feature_view_pb2 import FeatureViewArgs
from tecton_proto.args.feature_view_pb2 import FeatureViewType
from tecton_proto.args.new_transformation_pb2 import NewTransformationArgs
from tecton_proto.args.repo_metadata_pb2 import FeatureRepoSourceInfo
from tecton_proto.args.virtual_data_source_pb2 import VirtualDataSourceArgs
from tecton_proto.cli import repo_diff_pb2
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.common.id_pb2 import Id
from tecton_proto.data import state_update_pb2
from tecton_proto.metadataservice.metadata_service_pb2 import ApplyStateUpdateRequest
from tecton_proto.metadataservice.metadata_service_pb2 import NewStateUpdateRequest
from tecton_proto.metadataservice.metadata_service_pb2 import QueryStateUpdateRequest

UnwrappedFcoArgs = Union[
    VirtualDataSourceArgs,
    EntityArgs,
    NewTransformationArgs,
    FeatureViewArgs,
    FeatureServiceArgs,
]


_FCO_TYPE_TO_OBJECT_TYPE = {
    "virtual_data_source": repo_diff_pb2.TectonObjectType.DATA_SOURCE,
    "entity": repo_diff_pb2.TectonObjectType.ENTITY,
    "feature_view": repo_diff_pb2.TectonObjectType.FEATURE_VIEW,
    "feature_service": repo_diff_pb2.TectonObjectType.FEATURE_SERVICE,
    "transformation": repo_diff_pb2.TectonObjectType.TRANSFORMATION,
    "new_transformation": repo_diff_pb2.TectonObjectType.TRANSFORMATION,
}

_MATERIALIZABLE_FCO_TYPES = {
    "batch_feature_view",
    "stream_feature_view",
    "batch_window_aggregate_feature_view",
    "stream_window_aggregate_feature_view",
}


class PlanDiff:
    def __init__(
        self,
        fco_diffs: Iterable[state_update_pb2.FcoDiff],
        warnings: Iterable[state_update_pb2.ValidationMessage],
        plan_id: Id,
        suppress_warnings: bool,
        workspace_name: str,
    ):
        self.diffs = fco_diffs
        self.warnings = warnings
        self.plan_id = plan_id
        self.suppress_warnings = suppress_warnings
        self.workspace_name = workspace_name

        # preprocess warnings - group by fco id
        self.warnings_by_fco_id: Mapping[str, List[str]] = {}
        for warning in self.warnings:
            for fco_ref in warning.fco_refs:
                fco_id = IdHelper.to_string(fco_ref.fco_id)
                if fco_id not in self.warnings_by_fco_id:
                    self.warnings_by_fco_id[fco_id] = []
                self.warnings_by_fco_id[fco_id].append(warning.message)

    def print(self, debug: bool, recreates_suppressed: bool):
        """Pretty prints the plan diff in a human readable format.

        :param debug: If true, include Plan ID in output.
        :param recreates_suppressed: If true, print a warning after the plan to be careful when suppressing recreates.
        """
        if not self.has_diffs():
            printer.safe_print(
                Style.BRIGHT + "🎉 The remote and local state are the same, nothing to do! ", Style.RESET_ALL
            )
            return

        num_printed_warnings_total = 0
        printer.safe_print(Style.BRIGHT, "↓↓↓↓↓↓↓↓↓↓↓↓ Plan Start ↓↓↓↓↓↓↓↓↓↓", Style.RESET_ALL)
        printer.safe_print(Fore.RESET)
        for item in self.diffs:
            fco_id, _, _, _ = self._parse_plan_item(item)
            warnings = self._warnings_for_fco(fco_id) if fco_id else []
            num_printed_warnings = self._pprint_plan_item_with_warnings(item, warnings, self.suppress_warnings)
            num_printed_warnings_total = num_printed_warnings_total + num_printed_warnings
            printer.safe_print(Fore.RESET)

        printer.safe_print(Style.BRIGHT, "↑↑↑↑↑↑↑↑↑↑↑↑ Plan End ↑↑↑↑↑↑↑↑↑↑↑↑", Style.RESET_ALL)
        if not debug:
            printer.safe_print(
                Style.NORMAL, "Generated plan ID is %s" % IdHelper.to_string(self.plan_id), Style.RESET_ALL
            )
        printer.safe_print(
            Style.NORMAL,
            f"View your plan in the Web UI: {_cluster_url()}/app/{self.workspace_name}/plan-summary/{IdHelper.to_string(self.plan_id)}",
            Style.RESET_ALL,
        )

        if num_printed_warnings_total > 0 and not self.suppress_warnings:
            printer.safe_print(Style.BRIGHT, f"⚠️  Objects in plan contain warnings.", Style.RESET_ALL)

        if recreates_suppressed:
            printer.safe_print(
                Style.BRIGHT,
                Fore.RED,
                f"\n⚠️  ⚠️  ⚠️  WARNING: This plan was computed with --suppress-recreates which will force-apply "
                f"changes without recreating objects or rematerializing data. Feature schemas are unchanged, "
                f"but please triple check your plan output as this could cause changes in feature semantics. "
                f"Refer to https://docs.tecton.ai/ for full docs on --suppress-recreates.",
                Style.RESET_ALL,
            )

    def _warnings_for_fco(self, fco_id: str) -> List[str]:
        return self.warnings_by_fco_id[fco_id] if fco_id in self.warnings_by_fco_id else []

    def to_diff_summary_proto(self, debug: bool) -> repo_diff_pb2.TectonRepoDiffSummary:
        """Converts the plan diff to a summary proto.

        :param debug: If true, include Plan ID in proto.
        """
        repo_diff = repo_diff_pb2.TectonRepoDiffSummary()
        for fco_diff in self.diffs:
            repo_diff.object_diffs.append(self._convert_to_tecton_object_diff(fco_diff))
        if not debug:
            repo_diff.plan_id = IdHelper.to_string(self.plan_id)

        return repo_diff

    def confirm_plan_or_exit(self, interactive: bool):
        """Prompt the user to confirm the update.

        :param interactive: If true, display a yes/no prompt.
        """
        materialization_enabled = is_live_workspace(self.workspace_name)
        if materialization_enabled:
            if self._has_feature_service_update():
                printer.safe_print(
                    "Note: Updates to Feature Services may take up to 60 seconds to be propagated to the real-time feature-serving endpoint.",
                    file=sys.stderr,
                )

            if self._has_feature_view_update() and self._fco_diffs_has_materialization_job():
                printer.safe_print(
                    f'{Fore.YELLOW}Note: This workspace ("{self.workspace_name}") is a "Live" workspace. Applying this plan'
                    f" may result in new materialization jobs which will incur costs. Carefully examine the plan output before"
                    f" applying changes. {Fore.RESET}"
                )

        if interactive:
            confirm_or_exit(f'Are you sure you want to apply this plan to: "{self.workspace_name}"?')

    def has_diffs(self) -> bool:
        """Returns False if there are no changes in the diff."""
        if self.diffs:
            return True
        return False

    @property
    def num_fcos_changed(self) -> int:
        """Returns the number of FCOs being created, updated, or deleted."""
        count = 0
        for item in self.diffs:
            if item.type != state_update_pb2.FcoTransitionType.UNCHANGED:
                count += 1
        return count

    @property
    def id(self) -> Id:
        return self.plan_id

    def _has_feature_service_update(self) -> bool:
        for item in self.diffs:
            _, plan_type_item, fco_type, _ = self._parse_plan_item(item)
            if plan_type_item != "DELETE" and fco_type == "feature_service":
                return True
        return False

    def _has_feature_view_update(self) -> bool:
        for item in self.diffs:
            _, plan_type_item, fco_type, _ = self._parse_plan_item(item)
            # fco_type can be "stream_feature_view", "on_demand_feature_view", etc.
            if plan_type_item != "DELETE" and "feature_view" in fco_type:
                return True
        return False

    def _convert_to_tecton_object_diff(self, fco_diff: state_update_pb2.FcoDiff) -> repo_diff_pb2.TectonObjectDiff:
        object_diff = repo_diff_pb2.TectonObjectDiff()
        object_diff.transition_type = fco_diff.type

        fco_id, _, _, unwrapped_args = self._parse_plan_item(fco_diff)
        object_diff.object_metadata.name = unwrapped_args.info.name
        if unwrapped_args.info.owner:
            object_diff.object_metadata.owner = unwrapped_args.info.owner
        if unwrapped_args.info.description:
            object_diff.object_metadata.description = unwrapped_args.info.description

        object_diff.object_metadata.object_type = self._get_tecton_object_type(fco_diff)

        warnings = self._warnings_for_fco(fco_id) if fco_id else []
        for warning in warnings:
            object_diff.warnings.append(warning)

        return object_diff

    def _pprint_fields(self, args, colwidth):
        def pprint_metadata(indent, args):
            printer.safe_print(indent * " " + f'{"name:".ljust(colwidth)} {args.info.name}')
            if args.info.owner:
                printer.safe_print(indent * " " + f'{"owner:".ljust(colwidth)} {args.info.owner}')
            if args.info.description:
                printer.safe_print(indent * " " + f'{"description:".ljust(colwidth)} {args.info.description}')

        pprint_metadata(4, args)

    def _pprint_materialization_diff(self, item: state_update_pb2.FcoDiff):
        colwidth = 16
        indent = 4
        streaming_job = item.materialization_info.stream_task_diff
        recurring_batch_job = item.materialization_info.batch_task_diff
        backfill_jobs = item.materialization_info.backfill_task_diffs
        summary_list = []
        number_of_backfill_jobs = sum([backfill_job.number_of_jobs for backfill_job in backfill_jobs])
        if number_of_backfill_jobs == 1:
            summary_list.append("1 backfill")
        elif number_of_backfill_jobs > 1:
            summary_list.append(str(number_of_backfill_jobs) + " backfills")
        if streaming_job.display_string:
            summary_list.append("1 streaming")
        if recurring_batch_job.display_string:
            summary_list.append("1 recurring batch job")
        printer.safe_print(indent * " " + f"{'materialization:'.ljust(colwidth)} {', '.join(summary_list)}")
        if number_of_backfill_jobs > 0:
            printer.safe_print(indent * " " + f"{'> backfill:'.ljust(colwidth)} {backfill_jobs[0].display_string}")
            for backfill_job in backfill_jobs[1:]:
                printer.safe_print(indent * " " + f"{' '.ljust(colwidth)} {backfill_job.display_string}")
        incremental_prefix = "> incremental:"
        if streaming_job.display_string:
            printer.safe_print(indent * " " + f"{incremental_prefix.ljust(colwidth)} {streaming_job.display_string}")
            incremental_prefix = ""
        if recurring_batch_job.display_string:
            printer.safe_print(
                indent * " " + f"{incremental_prefix.ljust(colwidth)} {recurring_batch_job.display_string}"
            )

    def _pprint_plan_item_with_warnings(
        self, item: state_update_pb2.FcoDiff, warnings: List[str], suppress_warnings: bool
    ) -> int:
        """
        :return: number of warnings that were printed for this item
        """
        fco_id, plan_item_type, fco_type, unwrapped_args = self._parse_plan_item(item)
        indent = 2
        if plan_item_type == "CREATE":
            color = Fore.GREEN
            msg = f"+ Create {human_fco_type(fco_type)}"
        elif plan_item_type == "DELETE":
            color = Fore.RED
            msg = f"- Delete {human_fco_type(fco_type)}"
        elif plan_item_type == "UPGRADE":
            color = Fore.CYAN
            msg = f"~ Upgrade {human_fco_type(fco_type)} to the latest Tecton framework"
        elif plan_item_type == "UPDATE":
            color = Fore.YELLOW
            msg = f"~ Update {human_fco_type(fco_type)}"
        elif plan_item_type == "RECREATE":
            color = Fore.RED
            msg = f"~ Recreate (destructive) {human_fco_type(fco_type)}"
        else:
            assert False, f"Unknown item type {plan_item_type}"

        printer.safe_print((indent * " ") + color + msg + Fore.RESET)

        colwidth = 16
        self._pprint_fields(unwrapped_args, colwidth)

        diff_indent = 4
        for diff_item in item.diff:
            property_name_colwidth = max(len(diff_item.property_name) + 2, colwidth + 1)
            if len(diff_item.val_existing) + len(diff_item.val_declared) < 80:
                msg = (
                    (diff_item.property_name + ": ").ljust(property_name_colwidth)
                    + diff_item.val_existing
                    + " -> "
                    + diff_item.val_declared
                )
                printer.safe_print((diff_indent * " ") + color + msg + Fore.RESET)
            elif (
                diff_item.rendering_type == FcoPropertyRenderingType.FCO_PROPERTY_RENDERING_TYPE_PYTHON
                or diff_item.rendering_type == FcoPropertyRenderingType.FCO_PROPERTY_RENDERING_TYPE_SQL
            ):
                nl = "\n\n"
                diff = code_diff(diff_item, diff_indent)
                msg = (diff_item.property_name + ": ").ljust(property_name_colwidth) + nl + diff
                printer.safe_print((diff_indent * " ") + msg + Fore.RESET)
            else:
                nl = "\n" + ((diff_indent + 2) * " ")
                msg = (
                    (diff_item.property_name + ": ").ljust(property_name_colwidth)
                    + nl
                    + diff_item.val_existing
                    + nl
                    + " \u2B07\u2B07\u2B07\u2B07\u2B07 "
                    + nl
                    + diff_item.val_declared
                )
                printer.safe_print((diff_indent * " ") + color + msg + Fore.RESET)

        num_printed_warnings = 0
        # For DELETE transitions, we do not print warnings
        if plan_item_type != "DELETE" and len(warnings) > 0 and not suppress_warnings:
            for warning in warnings:
                num_printed_warnings = num_printed_warnings + 1
                printer.safe_print(
                    4 * " "
                    + Fore.YELLOW
                    + Style.BRIGHT
                    + f'{"warning:".ljust(colwidth)} {warning}'
                    + Fore.RESET
                    + Style.RESET_ALL
                )
        if self._fco_diff_has_materialization_job(item):
            self._pprint_materialization_diff(item)
        elif fco_type in _MATERIALIZABLE_FCO_TYPES:
            indent = 4
            printer.safe_print(indent * " " + f"{'materialization:'.ljust(colwidth)} No new materialization jobs")

        return num_printed_warnings

    def _fco_diff_has_materialization_job(self, diff_item: state_update_pb2.FcoDiff) -> bool:
        return bool(
            len(diff_item.materialization_info.backfill_task_diffs) > 0
            or diff_item.materialization_info.stream_task_diff.display_string
            or diff_item.materialization_info.batch_task_diff.display_string
        )

    def _fco_diffs_has_materialization_job(self) -> bool:
        return any(map(self._fco_diff_has_materialization_job, self.diffs))

    def _get_tecton_object_type(self, fco_diff: state_update_pb2.FcoDiff) -> repo_diff_pb2.TectonObjectType:
        if fco_diff.type == state_update_pb2.FcoTransitionType.CREATE:
            fco_type = fco_diff.declared_args.WhichOneof("args")
        else:
            fco_type = fco_diff.existing_args.WhichOneof("args")

        if fco_type not in _FCO_TYPE_TO_OBJECT_TYPE:
            raise errors.INTERNAL_ERROR(f"Error computing Tecton object type from FCO type: {fco_type}.")

        return _FCO_TYPE_TO_OBJECT_TYPE[fco_type]

    def _parse_plan_item(self, item: state_update_pb2.FcoDiff) -> Tuple[Optional[str], str, str, UnwrappedFcoArgs]:
        """
        :return: Parsed FcoDiff object:
                    - Client side FCO ID (Optional b/c FCO's with DELETE transition don't have client side id)
                    - Transition type
                    - FCO type
                    - Unwrapped FCO Args
        """
        plan_item_type = state_update_pb2.FcoTransitionType.Name(item.type)

        if item.HasField("declared_args"):  # DELETE transitions have no 'declared_args'
            fco_id, _, _ = self._unwrap_args(item.declared_args)
        else:
            fco_id = None

        if plan_item_type == "CREATE":
            fco_args = item.declared_args
        elif plan_item_type == "DELETE":
            fco_args = item.existing_args
        elif plan_item_type == "UPGRADE":
            fco_args = item.existing_args
        elif plan_item_type == "UPDATE":
            fco_args = item.existing_args
        elif plan_item_type == "RECREATE":
            fco_args = item.existing_args
        else:
            assert False, f"Unknown item type {plan_item_type}"

        _, fco_type, unwrapped_args = self._unwrap_args(fco_args)

        return fco_id, plan_item_type, fco_type, unwrapped_args

    def _unwrap_args(self, fco_args) -> Tuple[str, str, UnwrappedFcoArgs]:
        """
        :return: FCO arg properties:
                    - FCO ID
                    - FCO type
                    - UnwrappedFcoArgs object
        """
        fco_type = fco_args.WhichOneof("args")
        if fco_type == "virtual_data_source":
            unwrapped_args = fco_args.virtual_data_source
            if unwrapped_args.type == DataSourceType.BATCH:
                fco_type = "batch_data_source"
            elif unwrapped_args.type == DataSourceType.STREAM_WITH_BATCH:
                fco_type = "stream_data_source"
            fco_id = unwrapped_args.virtual_data_source_id
        elif fco_type == "entity":
            unwrapped_args = fco_args.entity
            fco_id = unwrapped_args.entity_id
        elif fco_type == "transformation":
            unwrapped_args = fco_args.transformation
            fco_id = unwrapped_args.transformation_id
        elif fco_type == "new_transformation":
            unwrapped_args = fco_args.new_transformation
            fco_id = unwrapped_args.transformation_id
        elif fco_type == "feature_view":
            unwrapped_args = fco_args.feature_view
            if unwrapped_args.feature_view_type == FeatureViewType.FEATURE_VIEW_TYPE_TEMPORAL:
                if unwrapped_args.temporal_args.data_source_type == DataSourceType.BATCH:
                    fco_type = "batch_feature_view"
                elif unwrapped_args.temporal_args.data_source_type == DataSourceType.STREAM_WITH_BATCH:
                    fco_type = "stream_feature_view"
            elif unwrapped_args.feature_view_type == FeatureViewType.FEATURE_VIEW_TYPE_TEMPORAL_AGGREGATE:
                if unwrapped_args.temporal_aggregate_args.data_source_type == DataSourceType.BATCH:
                    fco_type = "batch_window_aggregate_feature_view"
                elif unwrapped_args.temporal_aggregate_args.data_source_type == DataSourceType.STREAM_WITH_BATCH:
                    fco_type = "stream_window_aggregate_feature_view"
            elif unwrapped_args.feature_view_type == FeatureViewType.FEATURE_VIEW_TYPE_ON_DEMAND:
                fco_type = "on_demand_feature_view"
            fco_id = unwrapped_args.feature_view_id

        elif fco_type == "feature_service":
            unwrapped_args = fco_args.feature_service
            fco_id = unwrapped_args.feature_service_id
        else:
            assert False, f"Unknown object type: '{fco_type}'"

        # Currently, FeatureTable args are stored using FeatureViewArgs proto.
        # We differentiate between FeatureTable and FeatureView python classes here.
        if fco_type == "feature_view" and unwrapped_args.HasField("feature_table_args"):
            fco_type = "feature_table"

        return IdHelper.to_string(fco_id), fco_type, unwrapped_args


def get_declared_fco_args(objects) -> Tuple[List[FcoArgs], FeatureRepoSourceInfo]:
    all_args = []
    repo_source_info = FeatureRepoSourceInfo()

    for fco_obj in objects:
        fco_args = FcoArgs()
        args = fco_obj._args
        source_info = fco_obj._source_info
        if isinstance(fco_obj, BaseDataSource):
            source_info.fco_id.CopyFrom(args.virtual_data_source_id)
            fco_args.virtual_data_source.CopyFrom(args)
        elif isinstance(fco_obj, Entity):
            source_info.fco_id.CopyFrom(args.entity_id)
            fco_args.entity.CopyFrom(args)
        elif isinstance(fco_obj, Transformation):
            source_info.fco_id.CopyFrom(args.transformation_id)
            fco_args.new_transformation.CopyFrom(args)
        elif isinstance(fco_obj, FeatureDefinition):
            source_info.fco_id.CopyFrom(args.feature_view_id)
            fco_args.feature_view.CopyFrom(args)
        elif isinstance(fco_obj, FeatureService):
            source_info.fco_id.CopyFrom(args.feature_service_id)
            fco_args.feature_service.CopyFrom(args)
        else:
            assert False, f"Warning: unknown object{fco_obj}"

        all_args.append(fco_args)

        source_info.CopyFrom(source_info)
        repo_source_info.source_info.append(source_info)

    return all_args, repo_source_info


def dump_local_state(objects):
    with printer.safe_yaspin(Spinners.earth, text="Collecting local feature declarations") as sp:
        fco_args, repo_source_info = get_declared_fco_args(objects)
        sp.ok(printer.safe_string("✅"))

    request_plan = NewStateUpdateRequest()
    request_plan.request.fco_args.extend(fco_args)
    request_plan.request.repo_source_info.CopyFrom(repo_source_info)
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
                        f"\nUploading feature repo failed due to expired session. Please retry the command."
                    )
                else:
                    printer.safe_print(f"\nUploading feature repo failed with reason: {r.reason}")
                sys.exit(1)
            return
        except requests.RequestException as e:
            last_error = e
    else:
        raise SystemExit(last_error)


def update_tecton_state(
    objects,
    repo_files: List[Path],
    repo_root: str,
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
) -> TectonStateUpdateMetrics:
    # In debug mode we compute the plan synchronously, do not save it in the database, and do not allow to apply it.
    # Primary goal is allowing local development/debugging plans against remote clusters in read-only mode.
    assert not (debug and apply), "Cannot apply in debug mode"

    if apply and plan_id:
        # Applying an existing plan, so skip preparing args.
        state_id = IdHelper.from_string(plan_id)
        request_query = QueryStateUpdateRequest()
        request_query.state_id.CopyFrom(state_id)
        request_query.workspace = workspace_name

        try:
            response_query = metadata_service.instance().QueryStateUpdate(request_query)
        except (
            TectonInternalError,
            TectonAPIValidationError,
        ) as e:
            printer.safe_print(e)
            return TectonStateUpdateMetrics.from_error_message(str(e), suppress_recreates)

        if response_query.error:
            printer.safe_print(response_query.error)
            return TectonStateUpdateMetrics.from_error_message(response_query.error, suppress_recreates)
        if response_query.validation_result.errors:
            # Cannot pretty-print validation result using format_server_errors(), because collected local objects
            # might have changed since this plan was generated, so can't accurately match with this plan's FCOs.
            message = f"Cannot apply plan because it had errors."
            printer.safe_print(message)
            return TectonStateUpdateMetrics.from_error_message(message, suppress_recreates)
    else:
        with printer.safe_yaspin(Spinners.earth, text="Collecting local feature declarations") as sp:
            fco_args, repo_source_info = get_declared_fco_args(objects)
            sp.ok(printer.safe_string("✅"))

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

        server_side_msg_prefix = "Performing server-side feature validation: "
        with printer.safe_yaspin(Spinners.earth, text=f"{server_side_msg_prefix}: Initializing.") as sp:
            try:
                response_submit = metadata_service.instance().NewStateUpdate(request_plan)
                if response_submit.HasField("signed_url_for_repo_upload"):
                    upload_files(repo_files, repo_root, response_submit.signed_url_for_repo_upload)
                if response_submit.HasField("eager_response"):
                    response_query = response_submit.eager_response
                else:
                    seconds_slept = 0
                    request_query = QueryStateUpdateRequest()
                    request_query.workspace = workspace_name
                    request_query.state_id.CopyFrom(response_submit.state_id)
                    while True:
                        response_query = metadata_service.instance().QueryStateUpdate(request_query)
                        if response_query.latest_status_message:
                            sp.text = server_side_msg_prefix + response_query.latest_status_message
                        if response_query.ready:
                            break
                        seconds_to_sleep = 5
                        time.sleep(seconds_to_sleep)
                        seconds_slept += seconds_to_sleep
                        if seconds_slept > timeout_seconds:
                            sp.fail(printer.safe_string("⛔"))
                            printer.safe_print("Validation timed out.")
                            return TectonStateUpdateMetrics.from_error_message(
                                "Validation timed out.", suppress_recreates
                            )

                if response_query.error:
                    sp.fail(printer.safe_string("⛔"))
                    printer.safe_print(response_query.error)
                    return TectonStateUpdateMetrics.from_error_message(response_query.error, suppress_recreates)
                if response_query.validation_result.errors:
                    sp.fail(printer.safe_string("⛔"))
                    format_server_errors(response_query.validation_result.errors, objects, repo_root)
                    return TectonStateUpdateMetrics.from_error_message(
                        str(response_query.validation_result.errors), suppress_recreates
                    )
                sp.ok(printer.safe_string("✅"))
            except (
                TectonInternalError,
                TectonAPIValidationError,
            ) as e:
                sp.fail(printer.safe_string("⛔"))
                printer.safe_print(e)
                return TectonStateUpdateMetrics.from_error_message(str(e), suppress_recreates)

        state_id = response_submit.state_id

    plan_diff = PlanDiff(
        response_query.diff_items,
        response_query.validation_result.warnings,
        state_id,
        suppress_warnings,
        workspace_name,
    )

    plan_diff.print(debug, response_query.recreates_suppressed)

    if apply and plan_diff.has_diffs():
        # Use the workspace from the update request because the current workspace may have changed.
        plan_diff.confirm_plan_or_exit(interactive)

        request_apply = ApplyStateUpdateRequest()
        request_apply.state_id.CopyFrom(state_id)
        metadata_service.instance().ApplyStateUpdate(request_apply)

        printer.safe_print("🎉 all done!")

    if json_out_path:
        repo_diff_summary = plan_diff.to_diff_summary_proto(debug)
        json_out_path.parent.mkdir(parents=True, exist_ok=True)
        json_out_path.write_text(MessageToJson(repo_diff_summary))

    num_v3_fcos = sum(
        obj._args.version in (FrameworkVersion.UNSPECIFIED.value, FrameworkVersion.FWV3.value) for obj in objects
    )
    num_v5_fcos = sum(obj._args.version is FrameworkVersion.FWV5.value for obj in objects)

    return TectonStateUpdateMetrics(
        num_total_fcos=len(objects),
        num_fcos_changed=plan_diff.num_fcos_changed,
        num_v3_fcos=num_v3_fcos,
        num_v5_fcos=num_v5_fcos,
        # return full warnings for tests but only send the number of warnings to amplitude
        warnings=plan_diff.warnings,
        suppress_recreates=suppress_recreates,
        json_out=(json_out_path is not None),
    )
