from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from google.protobuf import duration_pb2
from typeguard import typechecked

from tecton_core import data_types as tecton_types
from tecton_core import feature_view_utils
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.common import aggregation_function_pb2 as afpb
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2


# Maps an aggregation proto to its respective simple string function name.
AGGREGATION_FUNCTIONS_TO_COLUMN_NAME = {
    afpb.AGGREGATION_FUNCTION_COUNT: "count",
    afpb.AGGREGATION_FUNCTION_SUM: "sum",
    afpb.AGGREGATION_FUNCTION_MEAN: "mean",
    afpb.AGGREGATION_FUNCTION_LAST: "last",
    afpb.AGGREGATION_FUNCTION_MIN: "min",
    afpb.AGGREGATION_FUNCTION_MAX: "max",
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: "var_samp",
    afpb.AGGREGATION_FUNCTION_VAR_POP: "var_pop",
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: "stddev_samp",
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: "stddev_pop",
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: "last_non_distinct_n",
    afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N: "lastn",
    afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N: "first_non_distinct_n",
    afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N: "first_distinct_n",
    afpb.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT: "approx_count_distinct",
    afpb.AGGREGATION_FUNCTION_APPROX_PERCENTILE: "approx_percentile",
}


# Maps a simple string aggregation function used to define feature views to its respective aggregation function proto.
AGGREGATION_FUNCTION_STR_TO_ENUM = {
    "stddev": afpb.AggregationFunction.AGGREGATION_FUNCTION_STDDEV_SAMP,
    "stddev_samp": afpb.AggregationFunction.AGGREGATION_FUNCTION_STDDEV_SAMP,
    "last": afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST,
    "count": afpb.AggregationFunction.AGGREGATION_FUNCTION_COUNT,
    "mean": afpb.AggregationFunction.AGGREGATION_FUNCTION_MEAN,
    "min": afpb.AggregationFunction.AGGREGATION_FUNCTION_MIN,
    "max": afpb.AggregationFunction.AGGREGATION_FUNCTION_MAX,
    "var_pop": afpb.AggregationFunction.AGGREGATION_FUNCTION_VAR_POP,
    "var_samp": afpb.AggregationFunction.AGGREGATION_FUNCTION_VAR_SAMP,
    "variance": afpb.AggregationFunction.AGGREGATION_FUNCTION_VAR_SAMP,  # variance is a var_samp alias.
    "stddev_pop": afpb.AggregationFunction.AGGREGATION_FUNCTION_STDDEV_POP,
    "sum": afpb.AggregationFunction.AGGREGATION_FUNCTION_SUM,
    "lastn": afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_DISTINCT_N,
    "last_non_distinct_n": afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
    "first_non_distinct_n": afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
    "first_distinct_n": afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_DISTINCT_N,
    "approx_count_distinct": afpb.AggregationFunction.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT,
    "approx_percentile": afpb.AggregationFunction.AGGREGATION_FUNCTION_APPROX_PERCENTILE,
}


def get_aggregation_enum_from_string(aggregation_function: str) -> afpb.AggregationFunction:
    aggregation_function_enum = AGGREGATION_FUNCTION_STR_TO_ENUM.get(aggregation_function, None)
    if aggregation_function_enum is None:
        msg = f"Unsupported aggregation function {aggregation_function}"
        raise ValueError(msg)
    return aggregation_function_enum


def get_aggregation_function_name(aggregation_function_enum):
    return AGGREGATION_FUNCTIONS_TO_COLUMN_NAME[aggregation_function_enum]


# Column prefixes that can't be derived from aggregation function name.
sum_of_squares_column_prefix = get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM) + "_of_squares"


def get_pretty_column_prefix(materialized_column_prefix: str):
    """Formats a materialized column prefix to be more human readable.

    For example, maps 'lastn10' to 'last_distinct_10' and 'last_non_distinct_n10' to 'last_10'.

    Only used for cosmetic purposes, to prettify the materialized column prefixes in the run API.
    """
    if materialized_column_prefix.startswith("lastn"):
        n = materialized_column_prefix.lstrip("lastn")
        return f"last_distinct_{n}"
    elif materialized_column_prefix.startswith("last_non_distinct_n"):
        n = materialized_column_prefix.lstrip("last_non_distinct_n")
        return f"last_{n}"
    elif materialized_column_prefix.startswith("first_non_distinct_n"):
        n = materialized_column_prefix.lstrip("first_non_distinct_n")
        return f"first_{n}"
    elif materialized_column_prefix.startswith("first_distinct_n"):
        n = materialized_column_prefix.lstrip("first_distinct_n")
        return f"first_distinct_{n}"

    return materialized_column_prefix


def get_materialization_aggregation_column_prefixes(
    aggregation_function_enum: afpb.AggregationFunction,
    function_params: Optional[
        Union[Dict[str, feature_view__args_pb2.ParamValue], afpb.AggregationFunctionParams]
    ] = None,
    is_continuous: bool = False,
) -> List[str]:
    """Maps an aggregation function to the prefixes that should be applied to the materialized columns.

    For example, the "sum" partial aggregation requires only a single column prefix, "sum", while the "mean" partial
    aggregation requires two column prefixes, "mean" and "count".

    The order of the column prefixes is important; it must match the order of the columns computed by the partial
    aggregate methods.

    For most aggregations, the prefixes should be the same for continuous and non-continuous.
    """
    if aggregation_function_enum not in _AGGREGATION_COLUMN_PREFIX_MAP:
        msg = f"Unsupported aggregation {aggregation_function_enum}"
        raise ValueError(msg)
    prefixes = _AGGREGATION_COLUMN_PREFIX_MAP[aggregation_function_enum]

    if not is_continuous and aggregation_function_enum in (
        afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_DISTINCT_N,
        afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
    ):
        if isinstance(function_params, afpb.AggregationFunctionParams):
            return [prefixes[0] + str(function_params.last_n.n)]

        assert function_params is not None, "function_params must be set for last N aggregations in non-continuous mode"
        return [prefixes[0] + str(function_params["n"].int64_value)]
    elif not is_continuous and aggregation_function_enum in (
        afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
        afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_DISTINCT_N,
    ):
        if isinstance(function_params, afpb.AggregationFunctionParams):
            return [prefixes[0] + str(function_params.first_n.n)]

        assert (
            function_params is not None
        ), "function_params must be set for first N aggregations in non-continuous mode"
        return [prefixes[0] + str(function_params["n"].int64_value)]

    return prefixes


# Sample and Population Standard Deviation and Variance only depend on sum of squares, count, and sum. For example, to
# calculate population variance you can divide the sum of squares by the count and subtract the square of the mean.
_var_stddev_prefixes = [
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM) + "_of_squares",
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT),
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM),
]

_approx_count_distinct_prefixes = [
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT) + "_indices",
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT) + "_registers",
]

_approx_percentile_prefixes = [
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_APPROX_PERCENTILE) + "_processed_means",
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_APPROX_PERCENTILE) + "_processed_weights",
]

_AGGREGATION_COLUMN_PREFIX_MAP = {
    afpb.AGGREGATION_FUNCTION_SUM: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM)],
    afpb.AGGREGATION_FUNCTION_MIN: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_MIN)],
    afpb.AGGREGATION_FUNCTION_MAX: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_MAX)],
    afpb.AGGREGATION_FUNCTION_COUNT: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT)],
    afpb.AGGREGATION_FUNCTION_LAST: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST)],
    afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N: [
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N)
    ],
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: [
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N)
    ],
    afpb.AGGREGATION_FUNCTION_MEAN: [
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_MEAN),
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT),
    ],
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: _var_stddev_prefixes,
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: _var_stddev_prefixes,
    afpb.AGGREGATION_FUNCTION_VAR_POP: _var_stddev_prefixes,
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: _var_stddev_prefixes,
    afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N: [
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N)
    ],
    afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N: [
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N)
    ],
    afpb.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT: _approx_count_distinct_prefixes,
    afpb.AGGREGATION_FUNCTION_APPROX_PERCENTILE: _approx_percentile_prefixes,
}


@typechecked
def aggregation_prefix_to_tecton_type(prefix: str) -> Optional[tecton_types.DataType]:
    prefix = prefix.lower()
    if prefix == "count":
        return tecton_types.Int64Type()
    elif prefix == "mean" or prefix == "sum_of_squares":
        return tecton_types.Float64Type()
    elif (
        prefix.startswith("lastn")
        or prefix.startswith("last_non_distinct_n")
        or prefix.startswith("first_non_distinct_n")
        or prefix.startswith("first_distinct_n")
    ):
        return tecton_types.ArrayType(tecton_types.StringType())
    else:
        return None


@typechecked
def get_materialization_column_name(prefix: str, input_column_name: str) -> str:
    return prefix + "_" + input_column_name


@typechecked
def create_aggregate_features(
    feature_aggregation: feature_view__args_pb2.FeatureAggregation,
    aggregation_interval_seconds: duration_pb2.Duration,
    is_continuous: bool,
) -> feature_view__data_pb2.AggregateFeature:
    """Build a AggregateFeature data proto from the input FeatureAggregation args proto."""
    feature_function = get_aggregation_enum_from_string(feature_aggregation.function.lower())
    assert feature_function, f"Unknown aggregation name: {feature_aggregation.function}"

    if feature_function in {
        afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_DISTINCT_N,
        afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
    }:
        function_params = afpb.AggregationFunctionParams(
            last_n=afpb.LastNParams(n=feature_aggregation.function_params["n"].int64_value)
        )
    elif feature_function in {
        afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_DISTINCT_N,
        afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
    }:
        function_params = afpb.AggregationFunctionParams(
            first_n=afpb.FirstNParams(n=feature_aggregation.function_params["n"].int64_value)
        )
    elif feature_function == afpb.AggregationFunction.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT:
        function_params = afpb.AggregationFunctionParams(
            approx_count_distinct=afpb.ApproxCountDistinctParams(
                precision=feature_aggregation.function_params["precision"].int64_value
            )
        )
    elif feature_function == afpb.AggregationFunction.AGGREGATION_FUNCTION_APPROX_PERCENTILE:
        function_params = afpb.AggregationFunctionParams(
            approx_percentile=afpb.ApproxPercentileParams(
                precision=feature_aggregation.function_params["precision"].int64_value,
                percentile=feature_aggregation.function_params["percentile"].double_value,
            )
        )
    else:
        function_params = None

    if len(feature_aggregation.function_params) > 0:
        assert (
            function_params is not None
        ), "function_params in the data proto should not be None since it is a non-empty dictionary in the args proto"

    output_feature_name = feature_aggregation.name or feature_view_utils.construct_aggregation_output_feature_name(
        column=feature_aggregation.column,
        aggregation_function_str=feature_aggregation.function,
        params=feature_aggregation.function_params,
        window=feature_aggregation.time_window,
        aggregation_interval=aggregation_interval_seconds,
        is_continuous=is_continuous,
    )
    return feature_view__data_pb2.AggregateFeature(
        input_feature_name=feature_aggregation.column,
        output_feature_name=output_feature_name,
        function=feature_function,
        window=feature_aggregation.time_window,
        function_params=function_params,
    )
