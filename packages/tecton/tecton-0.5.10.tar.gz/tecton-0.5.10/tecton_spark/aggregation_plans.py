from typing import Callable
from typing import List

import attr
import pyspark
from pyspark import SparkContext
from pyspark.sql import Column
from pyspark.sql import functions
from pyspark.sql import WindowSpec
from pyspark.sql.functions import expr

from tecton_core.aggregation_utils import get_aggregation_function_name
from tecton_proto.common import aggregation_function_pb2 as afpb


# WARNING: If you're changing this class there's a good chance you need to change
# AggregationPlans.java. Please look over that file carefully.


@attr.s(auto_attribs=True)
class AggregationPlan(object):
    # The order of columns must be the same in:
    # * The return list in partial_aggregation_transform
    # * The arguments list in full_aggregation_transform
    # * materialized_column_prefixes
    partial_aggregation_transform: Callable[[pyspark.sql.Column], List[pyspark.sql.Column]]
    full_aggregation_transform: Callable[[List[pyspark.sql.Column], pyspark.sql.window.WindowSpec], pyspark.sql.Column]
    materialized_column_prefixes: List[str]

    feature_server_transform: afpb.AggregationFunction

    def materialized_column_names(self, input_column_name):
        return [f"{prefix}_{input_column_name}" for prefix in self.materialized_column_prefixes]


def get_aggregation_plan(
    aggregation_function, function_params: afpb.AggregationFunctionParams, is_continuous: bool, time_key: str
):
    plan = AGGREGATION_PLANS.get(aggregation_function, None)
    if plan is None:
        raise ValueError(f"Unsupported aggregation function {aggregation_function}")

    if callable(plan):
        return plan(time_key, function_params, is_continuous)
    else:
        return plan


def _simple_partial_aggregation_transform(spark_transform):
    return lambda col: [spark_transform(col)]


def _simple_full_aggregation_transform(spark_transform):
    return lambda cols, window: spark_transform(cols[0]).over(window)


def _simple_aggregation_plan(aggregation_function: afpb.AggregationFunction, spark_transform):
    return AggregationPlan(
        partial_aggregation_transform=_simple_partial_aggregation_transform(spark_transform),
        full_aggregation_transform=_simple_full_aggregation_transform(spark_transform),
        materialized_column_prefixes=[get_aggregation_function_name(aggregation_function)],
        feature_server_transform=aggregation_function,
    )


def LastNDistinctAgg(col1, col2, n):
    sc = SparkContext._active_spark_context
    udf_name = f"tecton_last_{n}_distinct"
    sc._jvm.com.tecton.udfs.spark3.LastNRegister().register(n, udf_name, True)
    return expr(f"{udf_name}({col1}, {col2})")


def LimitedListConcatAgg(col1, n):
    sc = SparkContext._active_spark_context
    udf_name = f"tecton_last_{n}"
    sc._jvm.com.tecton.udfs.spark3.LimitedListConcatRegister().register(n, udf_name)
    return expr(f"{udf_name}({col1})")


def _make_lastn_partial(time_key: str, n: int):
    def _lastn_partial(col):
        return [LastNDistinctAgg(time_key, col, n)]

    return _lastn_partial


def _make_lastn_full(n: int):
    def _lastn_full(column_name, window):
        col = LimitedListConcatAgg(column_name, n).over(window)
        return col

    return _lastn_full


def LastNNonDistinctAgg(col1, col2, n) -> Column:
    sc = SparkContext._active_spark_context
    udf_name = f"tecton_last_{n}_non_distinct"
    sc._jvm.com.tecton.udfs.spark3.LastNRegister().register(n, udf_name, False)
    return expr(f"{udf_name}({col1}, {col2})")


def _make_last_n_non_distinct_partial(time_key: str, n: int) -> Callable:
    def _last_n_non_distinct(col: str) -> List[Column]:
        return [LastNNonDistinctAgg(time_key, col, n)]

    return _last_n_non_distinct


def _make_last_n_non_distinct_full(n: int) -> Callable:
    def _last_n_non_distinct_full(cols: List[Column], window: WindowSpec) -> Column:
        return functions.reverse(
            functions.slice(functions.reverse(functions.flatten(functions.collect_list(cols[0]).over(window))), 1, n)
        )

    return _last_n_non_distinct_full


def _sum_with_default(columns, window):
    col = functions.sum(columns[0]).over(window)
    # Fill null
    col = functions.when(col.isNull(), functions.lit(0)).otherwise(col)
    return col


# population variation equation: Σ(x^2)/n - μ^2
def _var_pop_full_aggregation(cols, window):
    sum_of_squares_col, count_col, sum_col = cols
    return functions.sum(sum_of_squares_col).over(window) / functions.sum(count_col).over(window) - functions.pow(
        functions.sum(sum_col).over(window) / functions.sum(count_col).over(window), 2
    )


def _stddev_pop_full_aggregation(cols, window):
    return functions.sqrt(_var_pop_full_aggregation(cols, window))


# sample variation equation: (Σ(x^2) - (Σ(x)^2)/N)/N-1
def _var_samp_full_aggregation(cols, window):
    sum_of_squares_col, count_col, sum_col = cols
    total_count_col = functions.sum(count_col).over(window)
    # check if count is equal to 0 for divide by 0 errors
    var_samp_col = functions.when(
        total_count_col != 1,
        (
            functions.sum(sum_of_squares_col).over(window)
            - functions.pow(functions.sum(sum_col).over(window), 2) / total_count_col
        )
        / (total_count_col - functions.lit(1)),
    )
    return var_samp_col


def _stddev_samp_full_aggregation(cols, window):
    return functions.sqrt(_var_samp_full_aggregation(cols, window))


def _stddev_var_partial(col):
    return [
        functions.sum(functions.pow(col, 2)),
        functions.count(col),
        functions.sum(functions.col(col)),
    ]


stddev_var_materialized_column_prefixes = [
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM) + "_of_squares",
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT),
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM),
]

AGGREGATION_PLANS = {
    afpb.AGGREGATION_FUNCTION_SUM: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_SUM, functions.sum),
    afpb.AGGREGATION_FUNCTION_MIN: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MIN, functions.min),
    afpb.AGGREGATION_FUNCTION_MAX: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MAX, functions.max),
    afpb.AGGREGATION_FUNCTION_LAST: _simple_aggregation_plan(
        afpb.AGGREGATION_FUNCTION_LAST, lambda col: functions.last(col, ignorenulls=True)
    ),
    # Needs to use COUNT for partial and SUM for full aggregation
    afpb.AGGREGATION_FUNCTION_COUNT: AggregationPlan(
        partial_aggregation_transform=_simple_partial_aggregation_transform(functions.count),
        full_aggregation_transform=_sum_with_default,
        materialized_column_prefixes=[get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT)],
        feature_server_transform=afpb.AGGREGATION_FUNCTION_COUNT,
    ),
    afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N: lambda time_key, params, is_continuous: AggregationPlan(
        partial_aggregation_transform=_make_lastn_partial(time_key, params.last_n.n),
        full_aggregation_transform=_make_lastn_full(params.last_n.n),
        materialized_column_prefixes=[
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N)
            + (str(params.last_n.n) if not is_continuous else "")
        ],
        feature_server_transform=afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N,
    ),
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: lambda time_key, params, is_continuous: AggregationPlan(
        partial_aggregation_transform=_make_last_n_non_distinct_partial(time_key, params.last_n.n),
        full_aggregation_transform=_make_last_n_non_distinct_full(params.last_n.n),
        materialized_column_prefixes=[
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N)
            + (str(params.last_n.n) if not is_continuous else "")
        ],
        feature_server_transform=afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
    ),
    afpb.AGGREGATION_FUNCTION_VAR_POP: AggregationPlan(
        partial_aggregation_transform=lambda col: _stddev_var_partial(col),
        full_aggregation_transform=_var_pop_full_aggregation,
        materialized_column_prefixes=stddev_var_materialized_column_prefixes,
        feature_server_transform=afpb.AGGREGATION_FUNCTION_VAR_POP,
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: AggregationPlan(
        partial_aggregation_transform=lambda col: _stddev_var_partial(col),
        full_aggregation_transform=_stddev_pop_full_aggregation,
        materialized_column_prefixes=stddev_var_materialized_column_prefixes,
        feature_server_transform=afpb.AGGREGATION_FUNCTION_STDDEV_POP,
    ),
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: AggregationPlan(
        partial_aggregation_transform=lambda col: _stddev_var_partial(col),
        full_aggregation_transform=_var_samp_full_aggregation,
        materialized_column_prefixes=stddev_var_materialized_column_prefixes,
        feature_server_transform=afpb.AGGREGATION_FUNCTION_VAR_SAMP,
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: AggregationPlan(
        partial_aggregation_transform=lambda col: _stddev_var_partial(col),
        full_aggregation_transform=_stddev_samp_full_aggregation,
        materialized_column_prefixes=stddev_var_materialized_column_prefixes,
        feature_server_transform=afpb.AGGREGATION_FUNCTION_STDDEV_SAMP,
    ),
}


def _mean_full_aggregation(cols, window):
    # Window aggregation doesn't work with more than one built-in function like this
    #   sum(mean_clicked * count_clicked) / sum(count_clicked)
    # And it does not support UDFs on bounded windows (the kind we use)
    #   https://issues.apache.org/jira/browse/SPARK-22239
    # We work around this limitations by calculating ratio over two window aggregations
    mean_col, count_col = cols
    return functions.sum(mean_col * count_col).over(window) / functions.sum(count_col).over(window)


# It is important that `partial_aggregation_transform` or `materialized_column_prefixes`
# contain aggregation data in the same ordering.
AGGREGATION_PLANS[afpb.AGGREGATION_FUNCTION_MEAN] = AggregationPlan(
    partial_aggregation_transform=lambda col: [functions.mean(col), functions.count(col)],
    full_aggregation_transform=_mean_full_aggregation,
    materialized_column_prefixes=[
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_MEAN),
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT),
    ],
    feature_server_transform=afpb.AGGREGATION_FUNCTION_MEAN,
)
