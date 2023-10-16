import sys
from abc import ABC
from abc import abstractmethod
from abc import abstractproperty
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

from colorama import Fore
from colorama import Style
from google.protobuf.json_format import MessageToJson

from tecton._internals import errors
from tecton.cli import printer
from tecton.cli.command import _cluster_url
from tecton_core.id_helper import IdHelper
from tecton_proto.args.diff_options_pb2 import FcoPropertyRenderingType
from tecton_proto.args.entity_pb2 import EntityArgs
from tecton_proto.args.feature_service_pb2 import FeatureServiceArgs
from tecton_proto.args.feature_view_pb2 import FeatureViewArgs
from tecton_proto.args.feature_view_pb2 import FeatureViewType
from tecton_proto.args.transformation_pb2 import TransformationArgs
from tecton_proto.args.virtual_data_source_pb2 import VirtualDataSourceArgs
from tecton_proto.cli import repo_diff_pb2
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.common.id_pb2 import Id
from tecton_proto.data import state_update_pb2
from tecton_proto.data.state_update_pb2 import FcoTransitionSideEffectStreamRestartType
from tecton_proto.metadataservice.metadata_service_pb2 import QueryStateUpdateResponseV2

from .cli_utils import code_diff
from .cli_utils import human_fco_type


UnwrappedFcoArgs = Union[
    VirtualDataSourceArgs,
    EntityArgs,
    TransformationArgs,
    FeatureViewArgs,
    FeatureServiceArgs,
]


_FCO_TYPE_TO_OBJECT_TYPE = {
    "virtual_data_source": repo_diff_pb2.TectonObjectType.DATA_SOURCE,
    "entity": repo_diff_pb2.TectonObjectType.ENTITY,
    "feature_view": repo_diff_pb2.TectonObjectType.FEATURE_VIEW,
    "feature_service": repo_diff_pb2.TectonObjectType.FEATURE_SERVICE,
    "transformation": repo_diff_pb2.TectonObjectType.TRANSFORMATION,
}

_MATERIALIZABLE_FCO_TYPES = {
    "batch_feature_view",
    "stream_feature_view",
    "batch_window_aggregate_feature_view",
    "stream_window_aggregate_feature_view",
}

_EMPTY_PLAN_MESSAGE = "🎉 The remote and local state are the same, nothing to do! "


class BasePlanRenderingClient(ABC):
    """Base interface for plan rendering clients."""

    @abstractmethod
    def has_diffs(self) -> bool:
        """Returns True if there are any changes to be applied."""
        raise NotImplementedError

    @abstractmethod
    def print_empty_plan(self):
        """Print the no changes (empty plan) message to the console."""
        raise NotImplementedError

    @abstractmethod
    def print_plan(self):
        """Print the tecton plan output to the console."""
        raise NotImplementedError

    @abstractmethod
    def print_apply_warnings(self):
        """If tecton apply is run, print relevant plan-level warnings to console."""
        raise NotImplementedError

    @abstractmethod
    def get_json_plan_output(self) -> str:
        """Return plan output as json string."""
        raise NotImplementedError

    @abstractproperty
    def num_fcos_changed(self) -> int:
        """Returns the number of FCOs being created, updated, or deleted."""
        raise NotImplementedError


class ThinPlanRenderingClient(BasePlanRenderingClient):
    """
    This is the "thin" client that queries the V2 API endpoints (NewStateUpdateV2 and
    QueryStateUpdateV2) to get the fully-rendered plan output from the server.
    """

    def __init__(
        self,
        response: QueryStateUpdateResponseV2,
    ):
        self.response = response

    def has_diffs(self) -> bool:
        return self.num_fcos_changed > 0

    def print_plan(self):
        printer.safe_print(self.response.successful_plan_output.string_output)

    def print_empty_plan(self):
        printer.safe_print(_EMPTY_PLAN_MESSAGE)

    def print_apply_warnings(self):
        printer.safe_print(self.response.successful_plan_output.apply_warnings)

    def get_json_plan_output(self) -> str:
        return self.response.successful_plan_output.json_output

    @property
    def num_fcos_changed(self) -> int:
        return self.response.successful_plan_output.num_fcos_changed

    @property
    def num_warnings(self) -> int:
        return self.response.successful_plan_output.num_warnings


class ThickPlanRenderingClient(BasePlanRenderingClient):
    """
    This is the "thick" client that queries the V1 API endpoints (NewStateUpdate and
    QueryStateUpdate) and renders the tecton plan output by parsing through the fields
    in the responses.
    """

    def __init__(
        self,
        fco_diffs: Iterable[state_update_pb2.FcoDiff],
        warnings: Iterable[state_update_pb2.ValidationMessage],
        plan_id: Id,
        suppress_warnings: bool,
        workspace_name: str,
        is_live_workspace: bool,
        debug: bool,
        recreates_suppressed: bool,
    ):
        self.diffs = fco_diffs
        self.warnings = warnings
        self.plan_id = plan_id
        self.suppress_warnings = suppress_warnings
        self.workspace_name = workspace_name
        self.is_live_workspace = is_live_workspace
        self.debug = debug
        self.recreates_suppressed = recreates_suppressed

        # preprocess warnings - group by fco id
        self.warnings_by_fco_id: Mapping[str, List[str]] = {}
        for warning in self.warnings:
            for fco_ref in warning.fco_refs:
                fco_id = IdHelper.to_string(fco_ref.fco_id)
                if fco_id not in self.warnings_by_fco_id:
                    self.warnings_by_fco_id[fco_id] = []
                self.warnings_by_fco_id[fco_id].append(warning.message)

    def print_empty_plan(self):
        printer.safe_print(Style.BRIGHT + _EMPTY_PLAN_MESSAGE, Style.RESET_ALL)

    def print_plan(self):
        """Pretty prints the plan diff in a human readable format."""
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
        if not self.debug:
            printer.safe_print(
                Style.NORMAL, "Generated plan ID is %s" % IdHelper.to_string(self.plan_id), Style.RESET_ALL
            )
        printer.safe_print(
            Style.NORMAL,
            f"View your plan in the Web UI: {_cluster_url()}/app/{self.workspace_name}/plan-summary/{IdHelper.to_string(self.plan_id)}",
            Style.RESET_ALL,
        )

        if num_printed_warnings_total > 0 and not self.suppress_warnings:
            printer.safe_print(Style.BRIGHT, "⚠️  Objects in plan contain warnings.", Style.RESET_ALL)

        if self.recreates_suppressed and self.is_live_workspace:
            num_stream_restarts = 0
            num_streams_checkpoints_invalidated = 0
            for item in self.diffs:
                _, transition_type, _, _ = self._parse_plan_item(item)
                if transition_type == "UPDATE" and item.HasField("transition_side_effects"):
                    update_type_transition = self._update_side_effects_transition_display(item)
                    if "Restart Stream" in update_type_transition:
                        num_stream_restarts += 1
                    if "Checkpoints Invalidated" in update_type_transition:
                        num_streams_checkpoints_invalidated += 1

            printer.safe_print(
                Style.BRIGHT,
                Fore.RED,
                "\n⚠️  ⚠️  ⚠️  WARNING: This plan was computed with --suppress-recreates which will force-apply "
                "changes without recreating objects or rematerializing data. Feature schemas are unchanged, "
                "but please triple check your plan output as this could cause changes in feature semantics. "
                "Refer to https://docs.tecton.ai/ for full docs on --suppress-recreates.",
                Style.RESET_ALL,
            )

            if self.is_live_workspace and num_stream_restarts > 0:
                warning_message = f"\n{num_stream_restarts} streaming materialization job(s) will be restarted. "
                if num_streams_checkpoints_invalidated > 0:
                    warning_message += (
                        f"Of those streams, checkpoints for {num_streams_checkpoints_invalidated} "
                        f"will no longer be valid-- the stream will take time to catch up, so please "
                        f"ensure the stream retention and watermark delay are at least 1 day to "
                        f"avoid potential data loss."
                    )
                printer.safe_print(Style.BRIGHT, Fore.RED, warning_message, Style.RESET_ALL)

    def _warnings_for_fco(self, fco_id: str) -> List[str]:
        return self.warnings_by_fco_id[fco_id] if fco_id in self.warnings_by_fco_id else []

    @property
    def num_warnings(self) -> int:
        return len(self.warnings)

    def get_json_plan_output(self) -> str:
        """Converts the plan diff to a summary proto."""
        repo_diff = repo_diff_pb2.TectonRepoDiffSummary()
        for fco_diff in self.diffs:
            repo_diff.object_diffs.append(self._convert_to_tecton_object_diff(fco_diff))
        if not self.debug:
            repo_diff.plan_id = IdHelper.to_string(self.plan_id)

        return MessageToJson(repo_diff)

    def print_apply_warnings(self):
        """If tecton apply is run, show relevant plan-level warnings."""
        materialization_enabled = self.is_live_workspace
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
            update_transition_string = "Update"
            if self.is_live_workspace and item.HasField("transition_side_effects"):
                update_transition_string = self._update_side_effects_transition_display(item)
            msg = f"~ {update_transition_string} {human_fco_type(fco_type)}"
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
            if diff_item.rendering_type == FcoPropertyRenderingType.FCO_PROPERTY_RENDERING_TYPE_HIDDEN:
                continue
            if len(diff_item.val_existing) + len(diff_item.val_declared) < 80:
                if diff_item.rendering_type == FcoPropertyRenderingType.FCO_PROPERTY_RENDERING_TYPE_REDACTED:
                    diff_item.val_existing = "[REDACTED]" if diff_item.val_existing else diff_item.val_existing
                    diff_item.val_declared = "[REDACTED]" if diff_item.val_declared else diff_item.val_declared
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
            msg = f"Error computing Tecton object type from FCO type: {fco_type}."
            raise errors.INTERNAL_ERROR(msg)

        return _FCO_TYPE_TO_OBJECT_TYPE[fco_type]

    def _update_side_effects_transition_display(self, item: state_update_pb2.FcoDiff) -> str:
        stream_restart_type = FcoTransitionSideEffectStreamRestartType.Name(
            item.transition_side_effects.stream_restart_type
        )
        if stream_restart_type == "RESTART_STREAM_REUSE_CHECKPOINTS":
            return "Restart Stream (Re-use Checkpoints)"
        elif stream_restart_type == "RESTART_STREAM_CHECKPOINTS_INVALIDATED":
            return "Restart Stream (Checkpoints Invalidated)"
        else:
            assert False, f"Unknown Update side effect {item.transition_side_effects.stream_restart_type}"

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
            elif unwrapped_args.type in (DataSourceType.PUSH_NO_BATCH, DataSourceType.PUSH_WITH_BATCH):
                fco_type = "push_source"
            fco_id = unwrapped_args.virtual_data_source_id
        elif fco_type == "entity":
            unwrapped_args = fco_args.entity
            fco_id = unwrapped_args.entity_id
        elif fco_type == "transformation":
            unwrapped_args = fco_args.transformation
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
