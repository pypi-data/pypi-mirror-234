from typing import List
from typing import Mapping

from google.protobuf import duration_pb2
from typeguard import typechecked

from tecton_core.time_utils import to_human_readable_str
from tecton_core.time_utils import to_positive_proto
from tecton_core.time_window_wrapper import TimeWindowWrapper
from tecton_proto.args import feature_view_pb2
from tecton_proto.common.schema_pb2 import Schema as SchemaProto


CONTINUOUS_MODE_BATCH_INTERVAL = duration_pb2.Duration(seconds=86400)


def get_input_feature_columns(view_schema: SchemaProto, join_keys: List[str], timestamp_key: str) -> List[str]:
    column_names = (c.name for c in view_schema.columns)
    return [c for c in column_names if c not in join_keys and c != timestamp_key]


def construct_aggregation_interval_name(aggregation_interval: duration_pb2.Duration, is_continuous: bool) -> str:
    if is_continuous:
        return "continuous"
    else:
        return to_human_readable_str(aggregation_interval)


@typechecked
def construct_aggregation_output_feature_name(
    column: str,
    aggregation_function_str: str,
    params: Mapping[str, feature_view_pb2.ParamValue],
    time_window: TimeWindowWrapper,
    aggregation_interval: duration_pb2.Duration,
    is_continuous: bool,
) -> str:
    """Constructs the name for the output feature column of an aggregation.

    For example, "VALUE_sum_7d_1d" or "VALUE_sum_7d_continuous".
    """
    aggregation_function_resolved_str = _resolve_function_name(aggregation_function_str, params)
    window_name = to_human_readable_str(time_window.window_duration)
    aggregation_interval_name = construct_aggregation_interval_name(aggregation_interval, is_continuous)

    column_name = f"{column}_{aggregation_function_resolved_str}_{window_name}_{aggregation_interval_name}".replace(
        " ", ""
    )

    offset_name = (
        "offset_" + to_human_readable_str(to_positive_proto(time_window.window_end))
        if time_window.window_end.seconds != 0
        else ""
    )

    if offset_name:
        column_name = f"{column_name}_{offset_name}"

    return column_name


def _resolve_function_name(aggregation_function_str: str, params: Mapping[str, feature_view_pb2.ParamValue]) -> str:
    if aggregation_function_str == "lastn":
        return f"last_distinct_{params['n'].int64_value}"
    elif aggregation_function_str == "last_non_distinct_n":
        return f"last_{params['n'].int64_value}"
    elif aggregation_function_str == "first_non_distinct_n":
        return f"first_{params['n'].int64_value}"
    elif aggregation_function_str == "first_distinct_n":
        return f"first_distinct_{params['n'].int64_value}"
    elif aggregation_function_str == "approx_percentile":
        percentile_str = str(params["percentile"].double_value)
        return f"approx_percentile_p{percentile_str.replace('.', '_')}"
    else:
        return aggregation_function_str
