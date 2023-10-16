from base64 import b64encode
from datetime import datetime
from io import BytesIO
from typing import List
from typing import Optional
from typing import Union

import pandas as pd
import pendulum
import requests
from pyspark.sql import DataFrame as pysparkDF
from pyspark.sql.functions import struct
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType
from pyspark.sql.types import DoubleType
from pyspark.sql.types import FloatType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import LongType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructType

from tecton._internals import data_frame_helper
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import utils
from tecton._internals.display import Displayable
from tecton._internals.feature_retrieval_internal import get_features
from tecton._internals.sdk_decorators import sdk_public_method
from tecton.fco import Fco
from tecton.interactive.data_frame import TectonDataFrame
from tecton.interactive.dataset import Dataset
from tecton.tecton_context import TectonContext
from tecton_core import conf
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.id_helper import IdHelper
from tecton_core.logger import get_logger
from tecton_core.online_serving_index import OnlineServingIndex
from tecton_core.pipeline_common import find_dependent_feature_set_items
from tecton_core.query import builder
from tecton_core.schema import Schema
from tecton_proto.data.materialization_status_pb2 import DataSourceType
from tecton_proto.data.materialization_status_pb2 import MaterializationStatus
from tecton_proto.metadataservice.metadata_service_pb2 import DeleteEntitiesRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetDeleteEntitiesInfoRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetFeatureFreshnessRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetFeatureViewSummaryRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetMaterializationStatusRequest
from tecton_proto.online_store.feature_value_pb2 import FeatureValueList
from tecton_proto.online_store.feature_value_pb2 import NullValue
from tecton_spark.schema_spark_utils import column_name_spark_data_types
from tecton_spark.schema_spark_utils import schema_from_spark
from tecton_spark.spark_helper import check_spark_version

logger = get_logger("FeatureDefinition")


class FeatureDefinition(Fco):
    @property
    def _fco_metadata(self):
        return self._proto.fco_metadata

    @property
    def _view_schema(self):
        return Schema(self._proto.schemas.view_schema)

    @property
    def _materialization_schema(self):
        return Schema(self._proto.schemas.materialization_schema)

    @property
    def _id_proto(self):
        return self._proto.feature_view_id

    @property  # type: ignore
    @sdk_public_method
    def id(self) -> str:
        """
        Returns the id of this object
        """
        return IdHelper.to_string(self._id_proto)

    @property
    def join_keys(self) -> List[str]:
        """
        Returns the join key column names
        """
        return list(self._proto.join_keys)

    @property  # type: ignore
    @sdk_public_method
    def online_serving_index(self) -> OnlineServingIndex:
        """
        Returns Defines the set of join keys that will be indexed and queryable during online serving.
        Defaults to the complete join key.
        """
        return OnlineServingIndex.from_proto(self._proto.online_serving_index)

    @property
    def wildcard_join_key(self) -> Optional[str]:
        """
        Returns a wildcard join key column name if it exists;
        Otherwise returns None.
        """
        online_serving_index = self.online_serving_index
        wildcard_keys = [join_key for join_key in self.join_keys if join_key not in online_serving_index.join_keys]
        return wildcard_keys[0] if wildcard_keys else None

    @property  # type: ignore
    @sdk_public_method
    def entity_names(self) -> List[str]:
        """
        Returns the names of entities for this Feature View.
        """
        entity_protos = [self._fco_container.get_by_id(IdHelper.to_string(id)) for id in self._proto.entity_ids]
        return [entity.fco_metadata.name for entity in entity_protos]

    @property
    def data_source_names(self) -> List[str]:
        """
        Returns the names of the data sources for this Feature View.
        """
        fd = FeatureDefinitionWrapper(self._proto, self._fco_container)
        return [ds.fco_metadata.name for ds in fd.data_sources]

    @property
    def _timestamp_key(self) -> str:
        raise NotImplementedError

    @property  # type: ignore
    @sdk_public_method
    def features(self) -> List[str]:
        """
        Returns the names of the (output) features.
        """
        join_keys = self.join_keys
        timestamp_key = self._timestamp_key
        return [
            col_name
            for col_name in self._view_schema.column_names()
            if col_name not in join_keys and col_name != timestamp_key
        ]

    @property  # type: ignore
    @sdk_public_method
    def url(self) -> str:
        """
        Returns a link to the Tecton Web UI.
        """
        return self._proto.web_url

    @sdk_public_method
    def summary(self) -> Displayable:
        """
        Returns various information about this feature definition, including the most critical metadata such
        as the name, owner, features, etc.
        """
        request = GetFeatureViewSummaryRequest()
        request.fco_locator.id.CopyFrom(self._id_proto)
        request.fco_locator.workspace = self.workspace

        response = metadata_service.instance().GetFeatureViewSummary(request)

        return Displayable.from_fco_summary(response.fco_summary)

    def _construct_feature_set_config(self) -> FeatureSetConfig:
        feature_set_config = FeatureSetConfig()
        feature_set_config._add(FeatureDefinitionWrapper(self._proto, self._fco_container))
        # adding dependent feature views for odfv
        if self._proto.HasField("on_demand_feature_view"):
            inputs = find_dependent_feature_set_items(
                self._fco_container,
                self._proto.pipeline.root,
                visited_inputs={},
                fv_id=self.id,
                workspace_name=self.workspace,
            )
            feature_set_config._definitions_and_configs = feature_set_config._definitions_and_configs + inputs
        return feature_set_config

    # method overrided by OnDemandFeatureView class
    def _should_infer_timestamp_of_spine(
        self, timestamp_key: Optional[str], spine: Optional[Union[pysparkDF, pd.DataFrame]]
    ):
        return spine is not None and timestamp_key is None

    def _point_in_time_join(self, spine: pysparkDF, timestamp_key: Optional[str], from_source: bool) -> TectonDataFrame:
        is_live_workspace = utils.is_live_workspace(self.workspace)
        if not from_source and not is_live_workspace and not self._proto.HasField("on_demand_feature_view"):
            raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(self.name, self.workspace)

        if (
            not from_source
            and not self._proto.HasField("on_demand_feature_view")
            and not self._proto.materialization_enabled
        ):
            raise errors.FD_GET_FEATURES_MATERIALIZATION_DISABLED(self.name)

        feature_set_config = self._construct_feature_set_config()
        if self._proto.HasField("on_demand_feature_view"):
            utils.validate_spine_dataframe(spine, timestamp_key, list(self._request_context.arg_to_schema.keys()))
            # check for odfv with feature table input
            if any(fv.is_feature_table for fv in feature_set_config.feature_definitions):
                if not is_live_workspace:
                    raise errors.FV_WITH_FT_DEVELOPMENT_WORKSPACE
                elif from_source:
                    raise errors.FROM_SOURCE_WITH_FT
        else:
            utils.validate_spine_dataframe(spine, timestamp_key)

        if conf.get_bool("QUERYTREE_ENABLED") and (
            self.wildcard_join_key is None or self.wildcard_join_key in spine.columns
        ):
            fdw = FeatureDefinitionWrapper(self._proto, self._fco_container)
            dac = FeatureDefinitionAndJoinConfig.from_feature_definition(fdw)
            return TectonDataFrame._create(builder.build_spine_join_querytree(dac, spine, timestamp_key, from_source))
        else:
            spark = TectonContext.get_instance()._spark
            df = data_frame_helper.get_features_for_spine(
                spark, spine, feature_set_config, timestamp_key=timestamp_key, from_source=from_source
            )

            df = utils.filter_internal_columns(df)
            return TectonDataFrame._create(df)

    def _get_historical_features(
        self,
        spine: Optional[Union[pysparkDF, pd.DataFrame, TectonDataFrame]],
        timestamp_key: Optional[str],
        start_time: Optional[Union[pendulum.DateTime, datetime]],
        end_time: Optional[Union[pendulum.DateTime, datetime]],
        entities: Optional[Union[pysparkDF, pd.DataFrame, TectonDataFrame]],
        from_source: bool,
        save: bool,
        save_as: Optional[str],
    ) -> TectonDataFrame:
        check_spark_version(self._proto.materialization_params.batch_materialization)
        has_point_in_time_join_params = spine is not None
        has_get_features_params = start_time is not None or end_time is not None or entities is not None

        if has_point_in_time_join_params:
            if has_get_features_params:
                raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                    ["start_time", "end_time", "entities"], "the spine parameter is provided"
                )

            if isinstance(spine, pd.DataFrame):
                spark = TectonContext.get_instance()._spark
                spine = spark.createDataFrame(spine)
            elif isinstance(spine, TectonDataFrame):
                spine = spine.to_spark()
            if self._should_infer_timestamp_of_spine(timestamp_key, spine):
                timestamp_key = utils.infer_timestamp(spine)
            df = self._point_in_time_join(spine, timestamp_key, from_source)
        else:
            if timestamp_key is not None:
                raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                    ["timestamp_key"], "the spine parameter is not provided"
                )
            fd = FeatureDefinitionWrapper(self._proto, self._fco_container)
            df = get_features(
                fd,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
            )

        if save or save_as is not None:
            return Dataset._create(
                df=df,
                save_as=save_as,
                workspace=self.workspace,
                feature_definition_id=self.id,
                spine=spine,
                timestamp_key=timestamp_key,
            )
        return df

    def _deletion_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        materialization_attempts = self._get_materialization_status().materialization_attempts
        deletion_attempts = [
            attempt
            for attempt in materialization_attempts
            if attempt.data_source_type == DataSourceType.DATA_SOURCE_TYPE_DELETION
        ]
        column_names, materialization_status_rows = utils.format_materialization_attempts(
            deletion_attempts, verbose, limit, sort_columns, errors_only
        )

        return self._create_materialization_table(column_names, materialization_status_rows)

    def _materialization_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        materialization_attempts = self._get_materialization_status().materialization_attempts
        column_names, materialization_status_rows = utils.format_materialization_attempts(
            materialization_attempts, verbose, limit, sort_columns, errors_only
        )

        return self._create_materialization_table(column_names, materialization_status_rows)

    def _create_materialization_table(self, column_names, materialization_status_rows):
        print("All the displayed times are in UTC time zone")

        # Setting `max_width=0` creates a table with an unlimited width.
        table = Displayable.from_table(headings=column_names, rows=materialization_status_rows, max_width=0)
        # Align columns in the middle horizontally
        table._text_table.set_cols_align(["c" for _ in range(len(column_names))])

        return table

    def _get_materialization_status(self) -> MaterializationStatus:
        """
        Returns MaterializationStatus proto for the FeatureView.
        """
        request = GetMaterializationStatusRequest()
        request.feature_package_id.CopyFrom(self._id_proto)

        response = metadata_service.instance().GetMaterializationStatus(request)
        return response.materialization_status

    def _delete_keys(
        self,
        keys: Union[pysparkDF, pd.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> None:
        if not offline and not online:
            raise errors.NO_STORE_SELECTED
        fd = FeatureDefinitionWrapper(self._proto, self._fco_container)
        if offline and any([x.offline_enabled for x in self._proto.materialization_state_transitions]):
            if not fd.offline_store_config.HasField("delta"):
                raise errors.OFFLINE_STORE_NOT_SUPPORTED
        if isinstance(keys, pd.DataFrame):
            if len(keys) == 0:
                raise errors.EMPTY_ARGUMENT("join_keys")
            if len(keys.columns[keys.columns.duplicated()]):
                raise errors.DUPLICATED_COLS_IN_KEYS(", ".join(list(keys.columns)))
            spark_df = self._convert_pandas_to_spark_df(keys)
        elif isinstance(keys, pysparkDF):
            spark_df = keys
        else:
            raise errors.INVALID_JOIN_KEY_TYPE(type(keys))
        utils.validate_entity_deletion_keys_dataframe(df=spark_df, join_keys=fd.join_keys, view_schema=fd.view_schema)
        is_live_workspace = utils.is_live_workspace(self.workspace)
        if not is_live_workspace:
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE("delete_keys")

        if online and all([not x.online_enabled for x in self._proto.materialization_state_transitions]):
            print("Online materialization was never enabled. No data to be deleted in online store.")
            online = False

        if offline and all([not x.offline_enabled for x in self._proto.materialization_state_transitions]):
            print("Offline materialization was never enabled. No data to be deleted in offline store.")
            offline = False

        if online or offline:
            self._send_delete_keys_request(keys, online, offline)

    def _freshness(self):
        fresh_request = GetFeatureFreshnessRequest()
        fresh_request.fco_locator.id.CopyFrom(self._id_proto)
        fresh_request.fco_locator.workspace = self.workspace
        return metadata_service.instance().GetFeatureFreshness(fresh_request)

    def _serialize_join_keys(self, spark_keys_df: pysparkDF):
        def serialize_fn(x):
            ret = FeatureValueList()
            for item in x:
                if isinstance(item, int):
                    ret.feature_values.add().int64_value = item
                elif isinstance(item, str):
                    ret.feature_values.add().string_value = item
                elif item is None:
                    ret.feature_values.add().null_value.CopyFrom(NullValue())
                else:
                    raise Exception(f"Unknown type: {type(item)}")
            return b64encode(ret.SerializeToString()).decode()

        serialize = udf(serialize_fn, StringType())
        return spark_keys_df.select(struct(*self.join_keys).alias("join_keys_array")).select(
            serialize("join_keys_array")
        )

    def _send_delete_keys_request(self, keys: Union[pysparkDF, pd.DataFrame], online: bool, offline: bool):

        info_request = GetDeleteEntitiesInfoRequest()
        info_request.feature_definition_id.CopyFrom(self._id_proto)
        info_response = metadata_service.instance().GetDeleteEntitiesInfo(info_request)
        s3_path = info_response.df_path
        online_join_keys_path = s3_path + "/online"
        offline_join_keys_path = s3_path + "/offline"
        deletion_request = DeleteEntitiesRequest()
        deletion_request.fco_locator.id.CopyFrom(self._id_proto)
        deletion_request.fco_locator.workspace = self.workspace
        deletion_request.online = online
        deletion_request.offline = offline
        deletion_request.online_join_keys_path = online_join_keys_path
        deletion_request.offline_join_keys_path = offline_join_keys_path
        if online:
            # We actually generate the presigned url but it's not used for online case
            spark = TectonContext.get_instance()._spark
            if isinstance(keys, pd.DataFrame):
                spark_keys_df = spark.createDataFrame(keys)
            else:
                spark_keys_df = keys
            spark_keys_df = spark_keys_df.distinct()
            join_key_df = self._serialize_join_keys(spark_keys_df)

            # coalesce(1) causes it to write to 1 file, but the jvm code
            # is actually robust to multiple files here
            join_key_df.coalesce(1).write.csv(online_join_keys_path)

        if offline:
            # We write in the native format and avoid converting Pandas <-> Spark due to partially incompatible
            # type system, in specifically missing Int in Pandas
            if isinstance(keys, pysparkDF):
                keys.write.parquet(offline_join_keys_path)
            else:
                upload_url = info_response.signed_url_for_df_upload_offline
                self._check_types_and_upload_df_pandas(upload_url, offline_join_keys_path, keys)

        metadata_service.instance().DeleteEntities(deletion_request)
        print(
            "A deletion job has been created. You can track the status of the job in the Web UI under Materialization section or with deletion_status(). The deletion jobs have a type 'Deletion'."
        )

    def _convert_pandas_to_spark_df(self, df: pd.DataFrame):
        tc = TectonContext.get_instance()
        spark = tc._spark
        spark_df = spark.createDataFrame(df)

        converted_schema = self._convert_ingest_schema(spark_df.schema)

        if converted_schema != spark_df.schema:
            spark_df = spark.createDataFrame(df, schema=converted_schema)

        return spark_df

    def _check_types_and_upload_df_pandas(self, upload_url: str, df_path: str, df: pd.DataFrame):
        if upload_url:
            self._upload_df_pandas(upload_url, df)
        elif df_path:
            spark_df = self._convert_pandas_to_spark_df(df)
            spark_df.write.parquet(df_path)

    def _convert_ingest_schema(self, ingest_schema: StructType) -> StructType:
        """
        The Pandas to Spark dataframe conversion implicitly derives the Spark schema. We handle converting/correcting
        for some type conversions where the derived schema and the feature table schema do not match.
        """
        ft_columns = column_name_spark_data_types(self._view_schema)
        ingest_columns = column_name_spark_data_types(schema_from_spark(ingest_schema))

        converted_ingest_schema = StructType()
        int_converted_columns = []

        for col_name, col_type in ingest_columns:
            if col_type == LongType() and (col_name, IntegerType()) in ft_columns:
                int_converted_columns.append(col_name)
                converted_ingest_schema.add(col_name, IntegerType())
            elif col_type == ArrayType(DoubleType()) and (col_name, ArrayType(FloatType())) in ft_columns:
                converted_ingest_schema.add(col_name, ArrayType(FloatType()))
            else:
                converted_ingest_schema.add(col_name, col_type)

        if int_converted_columns:
            logger.warning(
                f"Tecton is casting field(s) {', '.join(int_converted_columns)} to type Integer (was type Long). To remove this warning, use a Long type in the schema."
            )

        return converted_ingest_schema

    def _upload_df_pandas(self, upload_url: str, df: pd.DataFrame):
        out_buffer = BytesIO()
        df.to_parquet(out_buffer, index=False)

        # Maximum 1GB per ingestion
        if out_buffer.__sizeof__() > 1000000000:
            raise errors.FT_DF_TOO_LARGE

        r = requests.put(upload_url, data=out_buffer.getvalue())
        if r.status_code != 200:
            raise errors.FT_UPLOAD_FAILED(r.reason)
