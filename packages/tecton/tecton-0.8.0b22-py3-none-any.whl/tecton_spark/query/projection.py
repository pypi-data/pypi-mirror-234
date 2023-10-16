from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional

import attrs
import pendulum
import pyspark
import pyspark.sql.window as spark_window
from pyspark.sql import functions
from pyspark.sql.functions import expr

from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query_consts import ANCHOR_TIME
from tecton_core.query_consts import TECTON_UNIQUE_ID_COL
from tecton_spark.query.node import SparkExecNode
from tecton_spark.time_utils import convert_epoch_to_timestamp_column
from tecton_spark.time_utils import convert_timestamp_to_epoch


@attrs.frozen
class AddAnchorTimeSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_store_format_version: int
    batch_schedule: int
    timestamp_field: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        anchor_time_val = convert_timestamp_to_epoch(
            functions.col(self.timestamp_field), self.feature_store_format_version
        )
        df = input_df.withColumn(
            ANCHOR_TIME,
            anchor_time_val - anchor_time_val % self.batch_schedule,
        )
        return df


@attrs.frozen
class AddRetrievalAnchorTimeSparkNode(SparkExecNode):
    input_node: SparkExecNode
    name: str
    feature_store_format_version: int
    batch_schedule: int
    tile_interval: int
    timestamp_field: str
    is_stream: bool
    data_delay_seconds: Optional[int] = 0

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        anchor_time_val = convert_timestamp_to_epoch(
            functions.col(self.timestamp_field) - expr(f"interval {self.data_delay_seconds} seconds"),
            self.feature_store_format_version,
        )
        # tile_interval will be 0 for continuous
        if self.tile_interval == 0:
            df = input_df.withColumn(ANCHOR_TIME, anchor_time_val)
        else:
            # For stream, we use the tile interval for bucketing since the data is available as soon as
            # the aggregation interval ends.
            # For BAFV, we use the batch schedule to get the last tile written.
            if self.is_stream:
                df = input_df.withColumn(
                    ANCHOR_TIME,
                    anchor_time_val - anchor_time_val % self.tile_interval - self.tile_interval,
                )
            else:
                df = input_df.withColumn(
                    ANCHOR_TIME,
                    anchor_time_val - anchor_time_val % self.batch_schedule - self.tile_interval,
                )
        return df


@attrs.frozen
class RenameColsSparkNode(SparkExecNode):
    input_node: SparkExecNode
    mapping: Optional[Dict[str, str]]
    drop: Optional[List[str]]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        if self.mapping:
            for old_name, new_name in self.mapping.items():
                if new_name:
                    input_df = input_df.withColumnRenamed(old_name, new_name)
        if self.drop:
            for col in self.drop:
                input_df = input_df.drop(col)
        return input_df


@attrs.frozen
class ConvertEpochToTimestampSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_store_formats: Dict[str, int]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        for name, feature_store_format_version in self.feature_store_formats.items():
            input_df = input_df.withColumn(
                name,
                convert_epoch_to_timestamp_column(functions.col(name), feature_store_format_version),
            )
        return input_df


@attrs.frozen
class AddEffectiveTimestampSparkNode(SparkExecNode):
    input_node: SparkExecNode
    timestamp_field: str
    effective_timestamp_name: str
    batch_schedule_seconds: int
    is_stream: bool
    data_delay_seconds: int
    is_temporal_aggregate: bool

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)

        # batch_schedule = 0 implies feature table.
        if self.batch_schedule_seconds == 0 or self.is_stream:
            effective_timestamp = functions.col(self.timestamp_field)
        else:
            slide_str = f"{self.batch_schedule_seconds} seconds"
            timestamp_col = functions.col(self.timestamp_field)
            # Timestamp of temporal aggregate is end of the anchor time window. Subtract 1 micro
            # to get the correct bucket for batch schedule.
            if self.is_temporal_aggregate:
                timestamp_col -= expr("interval 1 microseconds")
            window_spec = functions.window(timestamp_col, slide_str, slide_str)
            effective_timestamp = window_spec.end + expr(f"interval {self.data_delay_seconds} seconds")

        df = input_df.withColumn(self.effective_timestamp_name, effective_timestamp)
        return df


@attrs.frozen
class AddDurationSparkNode(SparkExecNode):
    input_node: SparkExecNode
    timestamp_field: str
    duration: pendulum.Duration
    new_column_name: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)

        df = input_df.withColumn(
            self.new_column_name,
            functions.col(self.timestamp_field) + expr(f"interval {self.duration.total_seconds()} seconds"),
        )
        return df


@attrs.frozen
class SelectDistinctSparkNode(SparkExecNode):
    input_node: SparkExecNode
    columns: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return input_df.select(self.columns).distinct()


@attrs.frozen
class AggregationSecondaryKeyExplodeSparkNode(SparkExecNode):
    """
    This node returns all <entitiy, aggregation secondary key> pairs from the input node. It's used for retriving
    secondary key aggregate features without spine.

    This node is simliar to AsofSecondaryKeyExplodeSparkNode but doesn't require as-of join. It uses entities and
    anchor time to look back the max aggregation window time to find all secondary key values, and build a spine with
    all of them.
    """

    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper
    _tecton_temp_aggregation_secondary_key_col: ClassVar[str] = "_tecton_temp_agg_secondary_key_col"

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)

        window_spec = (
            spark_window.Window.partitionBy(self.fdw.join_keys)
            .orderBy([ANCHOR_TIME])
            .rangeBetween(self.fdw.earliest_anchor_time_from_window_start(), spark_window.Window.currentRow)
        )

        # Collect all secondary key values within the aggregation window, and explode them to build a spine.
        # Note the window based `collect_set` applies to every single row, so if a single join key has mutiple
        # aggregation secondary keys with the same anchor time, the result dataframe will have mutiple same rows for
        # that particular join key and anchor time. We select distinct here to deduplicate.
        input_df = (
            input_df.withColumn(
                self._tecton_temp_aggregation_secondary_key_col,
                functions.collect_set(self.fdw.aggregation_secondary_key).over(window_spec),
            )
            .drop(self.fdw.aggregation_secondary_key)
            .distinct()
        )
        return input_df.withColumn(
            self.fdw.aggregation_secondary_key, functions.explode(self._tecton_temp_aggregation_secondary_key_col)
        )


@attrs.frozen
class AddUniqueIdSparkNode(SparkExecNode):
    """
    Add a '_tecton_unique_id' column to the input node. This column is used to uniquely identify rows in the input node.

    Warning: The generated unique ID is non-deterministic on Spark, so this column may not be safe to join on.
    """

    input_node: SparkExecNode

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.input_node.to_dataframe(spark).withColumn(
            TECTON_UNIQUE_ID_COL, functions.monotonically_increasing_id()
        )
