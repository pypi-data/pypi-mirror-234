from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass
class AggregationFunction:
    name: str
    params: Dict[str, Union[int, float]]


# Last N aggregation that doesn't allow duplicates.
def last_distinct(n: int) -> AggregationFunction:
    if not isinstance(n, int):
        msg = "The parameter `n` of the last_distinct aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction("lastn", {"n": n})


# Last N aggregation that allows duplicates.
def last(n: int) -> AggregationFunction:
    if not isinstance(n, int):
        msg = "The parameter `n` of the last aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction("last_non_distinct_n", {"n": n})


# First N aggregation that doesn't allow duplicates.
def first_distinct(n: int) -> AggregationFunction:
    if not isinstance(n, int):
        msg = "The parameter `n` of the first_distinct aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction("first_distinct_n", {"n": n})


# First N aggregation that allows duplicates.
def first(n: int) -> AggregationFunction:
    if not isinstance(n, int):
        msg = "The parameter `n` of the first aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction("first_non_distinct_n", {"n": n})


def approx_count_distinct(precision: int = 8) -> AggregationFunction:
    if not isinstance(precision, int):
        msg = "The parameter `precision` of the approx_count_distinct aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction("approx_count_distinct", {"precision": precision})


def approx_percentile(percentile: float, precision: int = 100) -> AggregationFunction:
    if not isinstance(percentile, float):
        msg = "The parameter `percentile` of the approx_percentile aggregation must be a float."
        raise ValueError(msg)
    if not isinstance(precision, int):
        msg = "The parameter `precision` of the approx_percentile aggregation must be an integer."
        raise ValueError(msg)
    return AggregationFunction("approx_percentile", {"percentile": percentile, "precision": precision})
