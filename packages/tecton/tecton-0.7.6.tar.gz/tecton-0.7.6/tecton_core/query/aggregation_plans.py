from dataclasses import dataclass
from typing import Callable
from typing import List
from typing import Optional
from typing import Union

from pypika import Field
from pypika.analytics import Avg
from pypika.analytics import Count
from pypika.analytics import Max
from pypika.analytics import Min
from pypika.analytics import Sum
from pypika.analytics import WindowFrameAnalyticFunction
from pypika.functions import Cast
from pypika.functions import NullIf
from pypika.functions import Sqrt
from pypika.terms import LiteralValue
from pypika.terms import Term

from tecton_core.aggregation_utils import get_materialization_aggregation_column_prefixes
from tecton_proto.common import aggregation_function_pb2 as afpb


@dataclass
class QueryWindowSpec:
    partition_cols: List[str]
    order_by_col: str
    range_start: Union[str, WindowFrameAnalyticFunction.Edge]
    range_end: str


@dataclass
class AggregationPlan:
    """
    An AggregationPlan contains all the methods required to compute feature values for a specific Tecton aggregation.

    The order of the columns must be the same in:
    * the return list in partial_aggregation_query
    * the arguments list in full_aggregation_query
    * materialized_column_prefixes

    Attributes:
        partial_aggregation_query: A method that maps an input column name to a list of output pypika columns containing the partial aggregates.
        full_aggregation_query: A method that maps a list of input partial aggregate columns and a QueryWindowSpec to an output pypika column containing the full aggregates.
        materialized_column_prefixes: The list of prefixes that should be applied to the columns produced by `partial_aggregation_transform`.
    """

    partial_aggregation_query_terms: Callable[[str], List[Term]]
    full_aggregation_query_term: Callable[[List[str], QueryWindowSpec], Term]
    continuous_aggregation_query_terms: Optional[Callable[[str], List[Term]]]
    materialized_column_prefixes: List[str]

    def materialized_column_names(self, input_column_name: str) -> List[str]:
        return [f"{prefix}_{input_column_name}" for prefix in self.materialized_column_prefixes]


def _get_simple_window_query(
    col: str, query_window_spec: QueryWindowSpec, analytic_function: WindowFrameAnalyticFunction
):
    return (
        analytic_function(Field(col))
        .over(*[Field(x) for x in query_window_spec.partition_cols])
        .orderby(*[Field(query_window_spec.order_by_col)])
        .range(query_window_spec.range_start, query_window_spec.range_end)
    )


def _simple_aggregation_plan(
    aggregation_function: afpb.AggregationFunction, analytic_function: WindowFrameAnalyticFunction
):
    return AggregationPlan(
        partial_aggregation_query_terms=lambda col: [analytic_function(Field(col))],
        full_aggregation_query_term=lambda cols, query_window_spec: _get_simple_window_query(
            cols[0], query_window_spec, analytic_function
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(aggregation_function),
        continuous_aggregation_query_terms=lambda col: [Field(col)],
    )


def _mean_full_aggregation(cols: List[str], query_window_spec: QueryWindowSpec):
    mean_col, count_col = cols
    sum_query_term = (
        Sum(Field(mean_col) * Field(count_col))
        .over(*[Field(x) for x in query_window_spec.partition_cols])
        .orderby(*[Field(query_window_spec.order_by_col)])
        .range(query_window_spec.range_start, query_window_spec.range_end)
    )
    count_query_term = (
        Sum(Field(count_col))
        .over(*[Field(x) for x in query_window_spec.partition_cols])
        .orderby(*[Field(query_window_spec.order_by_col)])
        .range(query_window_spec.range_start, query_window_spec.range_end)
    )
    return sum_query_term / count_query_term


# sample variation equation: (Σ(x^2) - (Σ(x)^2)/N)/N-1
def _var_samp_full_aggregation(cols: List[str], query_window_spec: QueryWindowSpec):
    sum_of_squares_col, count_col, sum_col = cols
    count_query_term = Cast(
        (
            Sum(Field(count_col))
            .over(*[Field(x) for x in query_window_spec.partition_cols])
            .orderby(*[Field(query_window_spec.order_by_col)])
            .range(query_window_spec.range_start, query_window_spec.range_end)
        ),
        "double",
    )
    sum_of_squares_query_term = Cast(
        (
            Sum(Field(sum_of_squares_col))
            .over(*[Field(x) for x in query_window_spec.partition_cols])
            .orderby(*[Field(query_window_spec.order_by_col)])
            .range(query_window_spec.range_start, query_window_spec.range_end)
        ),
        "double",
    )
    sum_query_term = Cast(
        (
            Sum(Field(sum_col))
            .over(*[Field(x) for x in query_window_spec.partition_cols])
            .orderby(*[Field(query_window_spec.order_by_col)])
            .range(query_window_spec.range_start, query_window_spec.range_end)
        ),
        "double",
    )
    # check if count is equal to 0 for divide by 0 errors
    var_samp_col = (sum_of_squares_query_term - (sum_query_term**2) / count_query_term) / NullIf(
        count_query_term - 1, 0
    )
    return var_samp_col


def _var_pop_full_aggregation(cols: List[str], query_window_spec: QueryWindowSpec):
    sum_of_squares_col, count_col, sum_col = cols
    count_query_term = Cast(
        (
            Sum(Field(count_col))
            .over(*[Field(x) for x in query_window_spec.partition_cols])
            .orderby(*[Field(query_window_spec.order_by_col)])
            .range(query_window_spec.range_start, query_window_spec.range_end)
        ),
        "double",
    )
    sum_of_squares_query_term = Cast(
        (
            Sum(Field(sum_of_squares_col))
            .over(*[Field(x) for x in query_window_spec.partition_cols])
            .orderby(*[Field(query_window_spec.order_by_col)])
            .range(query_window_spec.range_start, query_window_spec.range_end)
        ),
        "double",
    )
    sum_query_term = Cast(
        (
            Sum(Field(sum_col))
            .over(*[Field(x) for x in query_window_spec.partition_cols])
            .orderby(*[Field(query_window_spec.order_by_col)])
            .range(query_window_spec.range_start, query_window_spec.range_end)
        ),
        "double",
    )
    return (sum_of_squares_query_term / count_query_term) - (sum_query_term / count_query_term) ** 2


def _stddev_samp_full_aggregation(cols: List[str], query_window_spec: QueryWindowSpec):
    return Sqrt(_var_samp_full_aggregation(cols, query_window_spec))


def _stddev_pop_full_aggregation(cols: List[str], query_window_spec: QueryWindowSpec):
    return Sqrt(_var_pop_full_aggregation(cols, query_window_spec))


def _mean_aggregation_plan():
    return AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Avg(Field(col)), Count(Field(col))],
        full_aggregation_query_term=lambda cols, query_window_spec: _mean_full_aggregation(cols, query_window_spec),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_MEAN),
        continuous_aggregation_query_terms=lambda col: [Cast(Field(col), "double"), Cast(LiteralValue("1"), "bigint")],
    )


AGGREGATION_PLANS = {
    afpb.AGGREGATION_FUNCTION_SUM: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_SUM, Sum),
    afpb.AGGREGATION_FUNCTION_MIN: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MIN, Min),
    afpb.AGGREGATION_FUNCTION_MAX: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MAX, Max),
    afpb.AGGREGATION_FUNCTION_COUNT: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Count(Field(col))],
        full_aggregation_query_term=lambda cols, query_window_spec: _get_simple_window_query(
            cols[0], query_window_spec, Sum
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_COUNT),
        continuous_aggregation_query_terms=lambda col: [Cast(LiteralValue("1"), "bigint")],
    ),
    afpb.AGGREGATION_FUNCTION_MEAN: _mean_aggregation_plan(),
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Sum(Field(col) ** 2), Count(Field(col)), Sum(Field(col))],
        full_aggregation_query_term=lambda cols, query_window_spec: _var_samp_full_aggregation(cols, query_window_spec),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_VAR_SAMP
        ),
        continuous_aggregation_query_terms=lambda col: [
            Cast(Field(col) ** 2, "double"),
            Cast(LiteralValue("1"), "bigint"),
            Cast(Field(col), "double"),
        ],
    ),
    afpb.AGGREGATION_FUNCTION_VAR_POP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Sum(Field(col) ** 2), Count(Field(col)), Sum(Field(col))],
        full_aggregation_query_term=lambda cols, query_window_spec: _var_pop_full_aggregation(cols, query_window_spec),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(afpb.AGGREGATION_FUNCTION_VAR_POP),
        continuous_aggregation_query_terms=lambda col: [
            Cast(Field(col) ** 2, "double"),
            Cast(LiteralValue("1"), "bigint"),
            Cast(Field(col), "double"),
        ],
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Sum(Field(col) ** 2), Count(Field(col)), Sum(Field(col))],
        full_aggregation_query_term=lambda cols, query_window_spec: _stddev_samp_full_aggregation(
            cols, query_window_spec
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_STDDEV_SAMP
        ),
        continuous_aggregation_query_terms=lambda col: [
            Cast(Field(col) ** 2, "double"),
            Cast(LiteralValue("1"), "bigint"),
            Cast(Field(col), "double"),
        ],
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: AggregationPlan(
        partial_aggregation_query_terms=lambda col: [Sum(Field(col) ** 2), Count(Field(col)), Sum(Field(col))],
        full_aggregation_query_term=lambda cols, query_window_spec: _stddev_pop_full_aggregation(
            cols, query_window_spec
        ),
        materialized_column_prefixes=get_materialization_aggregation_column_prefixes(
            afpb.AGGREGATION_FUNCTION_STDDEV_POP
        ),
        continuous_aggregation_query_terms=lambda col: [
            Cast(Field(col) ** 2, "double"),
            Cast(LiteralValue("1"), "bigint"),
            Cast(Field(col), "double"),
        ],
    ),
}
