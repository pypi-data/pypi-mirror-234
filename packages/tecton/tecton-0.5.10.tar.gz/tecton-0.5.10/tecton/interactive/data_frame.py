import time
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import attr
import numpy
import pandas
import pyspark
import pytz

from tecton._internals.rewrite import rewrite_tree_for_spine
from tecton._internals.sdk_decorators import sdk_public_method
from tecton_core import conf
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.rewrite import rewrite_tree
from tecton_spark.query import translate


def set_pandas_timezone_from_spark(pandas_df):
    """Match pandas timezone to that of Spark, s.t. the timestamps are correctly displayed."""
    from tecton.tecton_context import TectonContext

    tz = TectonContext.get_instance()._spark.conf.get("spark.sql.session.timeZone")
    for col in pandas_df.columns:
        if pandas.core.dtypes.common.is_datetime64_dtype(pandas_df[col]):
            pandas_df[col] = pandas_df[col].dt.tz_localize(pytz.timezone(tz))
            pandas_df[col] = pandas_df[col].dt.tz_convert(pytz.timezone("UTC"))
            pandas_df[col] = pandas_df[col].dt.tz_localize(None)
    return pandas_df


@attr.s(auto_attribs=True)
class FeatureVector(object):
    """
    FeatureVector Class.

    A FeatureVector is a representation of a single feature vector. Usage of a FeatureVector typically involves
    extracting the feature vector using ``to_pandas()``, ``to_dict()``, or ``to_numpy()``.

    """

    _names: List[str]
    _values: List[Union[int, str, bytes, float, list]]
    _effective_times: List[Optional[datetime]]
    slo_info: Optional[Dict[str, str]] = None

    @sdk_public_method
    def to_dict(
        self, return_effective_times: bool = False
    ) -> Dict[str, Union[int, str, bytes, float, list, dict, None]]:
        """Turns vector into a Python dict.

        :param: return_effective_times: Whether to return the effective time of the feature.

        :return: A Python dict.
        """
        if return_effective_times:
            return {
                name: {"value": self._values[i], "effective_time": self._effective_times[i]}
                for i, name in enumerate(self._names)
            }

        return dict(zip(self._names, self._values))

    @sdk_public_method
    def to_pandas(self, return_effective_times: bool = False) -> pandas.DataFrame:
        """Turns vector into a Pandas DataFrame.

        :param: return_effective_times: Whether to return the effective time of the feature as part of the DataFrame.

        :return: A Pandas DataFrame.
        """
        if return_effective_times:
            return pandas.DataFrame(
                list(zip(self._names, self._values, self._effective_times)), columns=["name", "value", "effective_time"]
            )

        return pandas.DataFrame([self._values], columns=self._names)

    @sdk_public_method
    def to_numpy(self, return_effective_times: bool = False) -> numpy.array:
        """Turns vector into a numpy array.

        :param: return_effective_times: Whether to return the effective time of the feature as part of the list.

        :return: A numpy array.
        """
        if return_effective_times:
            return numpy.array([self._values, self._effective_times])

        return numpy.array(self._values)

    def _update(self, other: "FeatureVector"):
        self._names.extend(other._names)
        self._values.extend(other._values)
        self._effective_times.extend(other._effective_times)


@attr.s(auto_attribs=True)
class TectonDataFrame(object):

    """
    A thin wrapper around Pandas and Spark dataframes.
    """

    _spark_df: Optional[pyspark.sql.DataFrame]
    _pandas_df: Optional[pandas.DataFrame]
    # TODO: Change the type to snowflake.snowpark.DataFrame, currently it will
    # fail type checking for our auto generated doc.
    _snowflake_df: Optional[Any] = None
    # should already by optimized
    _querytree: Optional[NodeRef] = None

    def _explain(self, extended: bool = False, show_ids=True):
        """Prints the query plan"""
        if self._spark_df:
            self._spark_df.explain(extended=extended)
        elif self._querytree:
            print(self._querytree.pretty_print(verbose=extended, show_ids=show_ids))
        elif self._snowflake_df:
            raise NotImplementedError
        else:
            print("No explain available")

    @sdk_public_method
    def to_spark(self) -> pyspark.sql.DataFrame:
        """Returns data as a Spark DataFrame.

        :return: A Spark DataFrame.
        """
        if self._spark_df is not None:
            return self._spark_df
        else:
            from tecton.tecton_context import TectonContext

            tc = TectonContext.get_instance()
            if self._querytree is not None:
                return translate.spark_convert(self._querytree).to_dataframe(tc._spark)
            elif self._pandas_df is not None:
                return tc._spark.createDataFrame(self._pandas_df)
            else:
                raise NotImplementedError

    @sdk_public_method
    def to_pandas(self) -> pandas.DataFrame:
        """Returns data as a Pandas DataFrame.

        :return: A Pandas DataFrame.
        """
        if self._pandas_df is not None:
            return self._pandas_df

        assert self._spark_df is not None or self._snowflake_df is not None or self._querytree is not None

        if self._spark_df is not None:
            return set_pandas_timezone_from_spark(self._spark_df.toPandas())

        if self._snowflake_df is not None:
            return self._snowflake_df.toPandas()

        if self._querytree is not None:
            return set_pandas_timezone_from_spark(self.to_spark().toPandas())

    @sdk_public_method
    def to_snowflake(self):
        """Returns data as a Snowflake DataFrame.

        :return: A Snowflake DataFrame.
        :meta private:
        """
        if self._snowflake_df is not None:
            return self._snowflake_df

        assert self._pandas_df is not None

        from tecton.snowflake_context import SnowflakeContext

        if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
            return SnowflakeContext.get_instance().get_session().createDataFrame(self._pandas_df)
        else:
            raise Exception("to_snowflake() is only available with Snowpark enabled")

    @classmethod
    def _create(cls, df: Union[pyspark.sql.DataFrame, pandas.DataFrame, NodeRef]):
        """Creates a Tecton DataFrame from a Spark or Pandas DataFrame."""
        if isinstance(df, pandas.DataFrame):
            return cls(spark_df=None, pandas_df=df, snowflake_df=None)
        elif isinstance(df, pyspark.sql.DataFrame):
            return cls(spark_df=df, pandas_df=None, snowflake_df=None)
        elif isinstance(df, NodeRef):
            rewrite_tree(df)

            from tecton.tecton_context import TectonContext

            spark = TectonContext.get_instance()._spark
            rewrite_tree_for_spine(df, spark)
            return cls(spark_df=None, pandas_df=None, snowflake_df=None, querytree=df)

        raise TypeError(f"DataFrame must be of type pandas.DataFrame or pyspark.sql.Dataframe, not {type(df)}")

    @classmethod
    # This should be merged into _create once snowpark is installed with pip
    def _create_with_snowflake(cls, df: "snowflake.snowpark.DataFrame"):
        """Creates a Tecton DataFrame from a Snowflake DataFrame."""
        from snowflake.snowpark import DataFrame as SnowflakeDataFrame

        if isinstance(df, SnowflakeDataFrame):
            return cls(spark_df=None, pandas_df=None, snowflake_df=df)

        raise TypeError(f"DataFrame must be of type snowflake.snowpark.Dataframe, not {type(df)}")

    @classmethod
    def _from_id(cls, x):
        """Creates a TectonDataFrame from a subtree of prior querytree labeled by an id in ._explain()."""
        from tecton_core.query.node_interface import global_map

        return cls._create(NodeRef(global_map[x]))

    def _timed_to_pandas(self):
        """Convenience method for measuring performance."""
        start = time.time()
        ret = self.to_spark().toPandas()
        end = time.time()
        print(f"took {end-start} seconds")
        return ret


# for legacy compat
DataFrame = TectonDataFrame
