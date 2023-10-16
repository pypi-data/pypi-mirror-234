from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Union

import numpy as np
import pandas
import pendulum
import pyspark
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery

import tecton
from tecton import conf
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import utils
from tecton._internals.sdk_decorators import sdk_public_method
from tecton.interactive import athena_api
from tecton.interactive import materialization_api
from tecton.interactive import snowflake_api
from tecton.interactive.data_frame import FeatureVector
from tecton.interactive.data_frame import TectonDataFrame
from tecton.interactive.feature_definition import FeatureDefinition
from tecton.interactive.materialization_api import MaterializationJobData
from tecton.interactive.query_helper import _QueryHelper
from tecton.interactive.run_api import run_batch
from tecton.interactive.run_api import run_ondemand
from tecton.interactive.run_api import run_stream
from tecton.tecton_context import TectonContext
from tecton_core import errors as core_errors
from tecton_core.fco_container import FcoContainer
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.feature_definition_wrapper import pipeline_to_transformation_ids
from tecton_core.logger import get_logger
from tecton_proto.args.feature_view_pb2 import BatchTriggerType
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.data import feature_view_pb2
from tecton_proto.data.new_transformation_pb2 import NewTransformation as TransformationProto
from tecton_proto.metadataservice.metadata_service_pb2 import GetFeatureViewRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetServingStatusRequest
from tecton_spark import pipeline_helper
from tecton_spark.materialization_params import MaterializationParams
from tecton_spark.pipeline_helper import find_request_context
from tecton_spark.schema_spark_utils import schema_to_spark
from tecton_spark.transformation import _RequestContext


def is_documented_by(original):
    def wrapper(target):
        target.__doc__ = original.__doc__
        return target

    return wrapper


__all__ = ["FeatureView", "get_feature_view"]


logger = get_logger("FeatureView")


class FeatureView(FeatureDefinition):
    """
    FeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    _proto: feature_view_pb2.FeatureView
    _fco_container: FcoContainer

    def __init__(self, proto, fco_container):
        """
        :param proto: FV proto
        :param fco_container: Contains all FV dependencies, e.g., Entities, DS-es, Transformations
        """
        self._proto = proto
        assert isinstance(fco_container, FcoContainer), type(fco_container)
        self._fco_container = fco_container

    # TODO:(samantha) delete this property
    @property
    def is_temporal_aggregate(self):
        """
        Deprecated. Please use the type property for this feature view.
        Returns whether or not this FeatureView is of type TemporalAggregateFeatureView.
        """
        logger.warning(
            "Deprecated. Please use the type property of this feature view or the built-in python type() method."
        )
        return self._proto.HasField("temporal_aggregate")

    # TODO:(samantha) delete this property
    @property
    def is_temporal(self):
        """
        Deprecated. Please use the type property for this feature view.
        Returns whether or not this FeatureView is of type TemporalFeatureView.
        """
        logger.warning(
            "Deprecated. Please use the type property of this feature view or the built-in python type() method."
        )
        return self._proto.HasField("temporal")

    # TODO:(samantha) delete this property
    @property
    def is_on_demand(self):
        """
        Deprecated. Please use the type property for this feature view.
        Returns whether or not this FeatureView is of type OnDemandFeatureView.
        """
        logger.warning(
            "Deprecated. Please use the type property of this feature view or the built-in python type() method."
        )
        return self._proto.HasField("on_demand_feature_view")

    @classmethod
    def _fco_type_name_singular_snake_case(cls) -> str:
        return "feature_view"

    @classmethod
    def _fco_type_name_plural_snake_case(cls) -> str:
        return "feature_views"

    def _fd_wrapper(self):
        return FeatureDefinitionWrapper(self._proto, self._fco_container)

    def __str__(self):
        return f"FeatureView|{self.id}"

    def __repr__(self):
        return f"FeatureView(name='{self.name}')"

    def _get_serving_status(self):
        request = GetServingStatusRequest()
        request.feature_package_id.CopyFrom(self._proto.feature_view_id)
        request.workspace = self.workspace
        return metadata_service.instance().GetServingStatus(request)

    @sdk_public_method
    def get_historical_features(
        self,
        spine: Optional[Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str]] = None,
        timestamp_key: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        entities: Optional[Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: bool = False,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> TectonDataFrame:
        """
        Returns a Tecton :class:`TectonDataFrame` of historical values for this feature view.
        If no arguments are passed in, all feature values for this feature view will be returned in a Tecton DataFrame.

        Note:
        The `timestamp_key` parameter is only applicable when a spine is passed in.
        Parameters `start_time`, `end_time`, and `entities` are only applicable when a spine is not passed in.

        :param spine: The spine to join against, as a dataframe.
            If present, the returned DataFrame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine.
            To distinguish between spine columns and feature columns, feature columns are labeled as
            `feature_view_name.feature_name` in the returned DataFrame.
            If spine is not specified, it'll return a DataFrame of feature values in the specified time range.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in the spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified, will default to the time column of the spine if there is only one present.
            If more than one time column is present in the spine, you must specify which column you'd like to use.
        :type timestamp_key: str
        :param start_time: The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type start_time: datetime.datetime
        :param end_time: The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type end_time: datetime.datetime
        :param entities: Filter feature data returned to a set of entity IDs.
            If specified, this DataFrame should only contain join key columns.
        :type entities: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param from_source: Whether feature values should be recomputed from the original data source.
            If False, we will read the materialized values from the offline store.
        :type from_source: bool
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: Name to save the DataFrame as.
            If unspecified and save=True, a name will be generated.
        :type save_as: str

        Examples:
            A FeatureView :py:mod:`fv` with join key :py:mod:`user_id`.

            1) :py:mod:`fv.get_historical_features(spine)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3],
            'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine.

            2) :py:mod:`fv.get_historical_features(spine, save_as='my_dataset)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine. Save the DataFrame as dataset with the name :py:mod`my_dataset`.

            3) :py:mod:`fv.get_historical_features(spine, timestamp_key='date_1')` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'date_2': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the 'date_1' column in the spine.

            4) :py:mod:`fv.get_historical_features(start_time=datetime(...), end_time=datetime(...))`
            Fetch all historical features from the offline store in the time range specified by `start_time` and `end_time`.

        :return: A Tecton :class:`TectonDataFrame`.
        """

        if self._proto.HasField("temporal") and self._proto.temporal.incremental_backfills:
            # We only allow from_source=False for Custom BFV.
            if not utils.is_live_workspace(self.workspace):
                raise errors.CBFV_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(self.name, self.workspace)

            if not self._proto.materialization_enabled:
                raise core_errors.FV_BFC_SINGLE_FROM_SOURCE

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
                append_prefix=False,
            )

        if conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED"):
            if not utils.is_live_workspace(self.workspace):
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE

            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
            )

        return self._get_historical_features(
            spine, timestamp_key, start_time, end_time, entities, from_source, save, save_as
        )

    @property
    def _timestamp_key(self) -> Optional[str]:
        if self._proto.HasField("timestamp_key"):
            return self._proto.timestamp_key
        return None

    @property
    def _writes_to_offline_feature_store(self) -> bool:
        """
        Returns if the FeatureView materialization is enabled to write to the OfflineStore.
        Return value does not reflect the completion of any specific materialization job.
        """
        return self._proto.materialization_enabled and self._proto.materialization_params.writes_to_offline_store

    @property
    def _writes_to_online_feature_store(self) -> bool:
        """
        Returns if the FeatureView materialization is enabled to write to the OnlineStore.
        Return value does not reflect the completion of any specific materialization job.
        """
        return self._proto.materialization_enabled and self._proto.materialization_params.writes_to_online_store

    @property
    def _materialization_params(self) -> Optional[MaterializationParams]:
        return MaterializationParams.from_proto(self._proto)

    @property  # type: ignore
    @sdk_public_method
    def feature_start_time(self) -> Optional[pendulum.DateTime]:
        """
        This represents the time at which features are first available.
        """
        if not self._proto.HasField("materialization_params") or not self._proto.materialization_params.HasField(
            "feature_start_timestamp"
        ):
            return None
        return pendulum.from_timestamp(self._proto.materialization_params.feature_start_timestamp.ToSeconds())

    def _batch_materialization_schedule(self) -> Optional[pendulum.Duration]:
        if not self._proto.HasField("materialization_params"):
            return None
        # TODO: this should return a formatted duration, not a timestamp
        return pendulum.Duration(seconds=self._proto.materialization_params.schedule_interval.ToSeconds())

    def _schedule_offset(self) -> Optional[pendulum.Duration]:
        if not self._proto.HasField("materialization_params"):
            return None
        schedule_offset = pendulum.duration(
            seconds=self._proto.materialization_params.allowed_upstream_lateness.ToSeconds()
        )
        if not schedule_offset:
            return None
        return schedule_offset

    @sdk_public_method
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> FeatureVector:
        """
        Returns a single Tecton :class:`tecton.FeatureVector` from the Online Store.

        :param join_keys: Join keys of the enclosed FeatureViews.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.

        Examples:
            A FeatureView :py:mod:`fv` with join key :py:mod:`user_id`.

            1) :py:mod:`fv.get_online_features(join_keys={'user_id': 1})`
            Fetch the latest features from the online store for user 1.

            2) :py:mod:`fv.get_online_features(join_keys={'user_id': 1}, include_join_keys_in_respone=True)`
            Fetch the latest features from the online store for user 1 and include the join key information (user_id=1) in the returned FeatureVector.

        :return: A :class:`tecton.FeatureVector` of the results.
        """
        if not self._writes_to_online_feature_store:
            raise errors.UNSUPPORTED_OPERATION(
                "get_online_features", "online_serving_enabled is not set to True for this FeatureView."
            )
        utils.validate_join_key_types(join_keys)

        return _QueryHelper(self._proto.fco_metadata.workspace, feature_view_name=self.name).get_feature_vector(
            join_keys or {},
            include_join_keys_in_response,
            {},
            self._request_context,
        )

    @property
    def _request_context(self) -> _RequestContext:
        return _RequestContext({})

    @property
    def _materialization_schema(self):
        from tecton_core.schema import Schema

        return Schema(self._proto.schemas.materialization_schema)

    @property
    def _dependent_transformation_protos(self) -> List[TransformationProto]:
        transformation_ids = pipeline_to_transformation_ids(self._proto.pipeline)
        return self._fco_container.get_by_ids(transformation_ids)

    def delete_keys(
        self,
        keys: Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> None:
        """
        Deletes any materialized data that matches the specified join keys from the FeatureView.
        This method kicks off a job to delete the data in the offline and online stores.
        If a FeatureView has multiple entities, the full set of join keys must be specified.
        Only supports Delta offline store and Dynamo online store.
        (offline_store=DeltaConfig() and online_store left as default)
        Maximum 500,000 keys can be deleted per request.

        :param keys: The Dataframe to be deleted. Must conform to the FeatureView join keys.
        :param online: (Optional, default=True) Whether or not to delete from the online store.
        :param offline: (Optional, default=True) Whether or not to delete from the offline store.
        :return: None if deletion job was created successfully.
        """
        return self._delete_keys(keys, online, offline)

    def deletion_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        """
        Displays information for deletion jobs created with the delete_keys() method,
        which may include past jobs, scheduled jobs, and job failures.

        :param verbose: If set to true, method will display additional low level deletion information,
            useful for debugging.
        :param limit: Maximum number of jobs to return.
        :param sort_columns: A comma-separated list of column names by which to sort the rows.
        :param: errors_only: If set to true, method will only return jobs that failed with an error.
        """
        return self._deletion_status(verbose, limit, sort_columns, errors_only)

    @property
    def _is_temporal_aggregate(self):
        return self._proto.HasField("temporal_aggregate")

    @property
    def _is_incremental(self):
        return self._proto.HasField("temporal") and self._proto.temporal.incremental_backfills

    @property  # type: ignore
    @sdk_public_method
    @is_documented_by(FeatureDefinition.features)
    def features(self) -> List[str]:
        if self._is_temporal_aggregate:
            return [
                f.output_feature_name
                for f in self._proto.temporal_aggregate.features
                if f.output_feature_name != self._timestamp_key
            ]
        return super().features

    @sdk_public_method
    @is_documented_by(materialization_api.cancel_materialization_job)
    def cancel_materialization_job(self, job_id: str) -> MaterializationJobData:
        return materialization_api.cancel_materialization_job(self.name, self.workspace, job_id)

    @sdk_public_method
    @is_documented_by(materialization_api.get_materialization_job)
    def get_materialization_job(self, job_id: str) -> MaterializationJobData:
        return materialization_api.get_materialization_job(self.name, self.workspace, job_id)

    @sdk_public_method
    @is_documented_by(materialization_api.list_materialization_jobs)
    def list_materialization_jobs(self) -> List[MaterializationJobData]:
        return materialization_api.list_materialization_jobs(self.name, self.workspace)


class OnDemandFeatureView(FeatureView):
    """
    OnDemandFeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    @sdk_public_method
    def run(
        self, **mock_inputs: Union[Dict[str, Any], pandas.DataFrame, DataFrame]
    ) -> Union[Dict[str, Any], "tecton.interactive.data_frame.TectonDataFrame"]:
        """
        Run the OnDemandFeatureView using mock inputs.

        :param \*\*mock_inputs: Required. Keyword args with the same expected keys
            as the OnDemandFeatureView's inputs parameters.
            For the "python" mode, each input must be a Dictionary representing a single row.
            For the "pandas" mode, each input must be a DataFrame with all of them containing the
            same number of rows and matching row ordering.

        Example:

        .. code-block:: python

            # Given a python on-demand feature view defined in your workspace:
            @on_demand_feature_view(
                sources=[transaction_request, user_transaction_amount_metrics],
                mode='python',
                schema=output_schema,
                description='The transaction amount is higher than the 1 day average.'
            )
            def transaction_amount_is_higher_than_average(request, user_metrics):
                return {'higher_than_average': request['amt'] > user_metrics['daily_average']}

        .. code-block:: python

            # Retrieve and run the feature view in a notebook using mock data:
            import tecton

            fv = tecton.get_workspace('prod').get_feature_view('transaction_amount_is_higher_than_average')

            result = fv.run(request={'amt': 100}, user_metrics={'daily_average': 1000})

            print(result)
            # {'higher_than_average': False}

        :return: A `Dict` object for the "python" mode and a tecton DataFrame of the results for the "pandas" mode.
        """
        # Snowflake compute uses the same code for run_ondemand as Spark.
        return run_ondemand(self._fd_wrapper(), self.name, mock_inputs)

    def _on_demand_transform_dataframe(
        self,
        spine: DataFrame,
        namespace_separator: str,
        use_materialized_data: bool = True,
        namespace: Optional[str] = None,
    ) -> DataFrame:
        """
        Adds features from an OnDemandFeatureView to the spine.

        :param spine: Spark dataframe used to compute the on-demand features. Any dependent feature values must already be a part of the spine.
        :param use_materialized_data: Use materialized data if materialization is enabled.

        :return: A spark dataframe containing the spine augmented with features. The features are prefixed by the namespace if it exists, or the FeatureView's name.
        """
        df = pipeline_helper.dataframe_with_input(
            pipeline=self._proto.pipeline,
            spark=TectonContext.get_instance()._spark,
            input_df=spine,
            output_schema=schema_to_spark(self._materialization_schema),
            transformations=self._dependent_transformation_protos,
            name=self.name,
            fv_id=self.id,
            namespace_separator=namespace_separator,
            namespace=namespace,
        )
        return df

    def _should_infer_timestamp_of_spine(
        self, timestamp_key: Optional[str], spine: Optional[Union[pandas.DataFrame, DataFrame]]
    ):
        if timestamp_key is not None:
            return False
        if spine is None:
            return False
        # normally odfvs don't depend on a timestamp key except for when they have dependent fvs
        # in this case we want to infer the timestamp key of the spine. A dependent fv can't be a odfv.
        return utils.get_num_dependent_fv(self._proto.pipeline.root, visited_inputs={}) > 0

    @sdk_public_method
    def get_historical_features(
        self,
        spine: Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: bool = False,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> TectonDataFrame:
        """
        Returns a Tecton :class:`TectonDataFrame` of historical values for this feature view.

        :param spine: The spine to join against, as a dataframe.
            The returned data frame will contain rollups for all (join key, request data key)
            combinations that are required to compute a full frame from the spine.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified and this feature view has feature view dependencies, `timestamp_key` will default to the time column of the spine if there is only one present.
        :type timestamp_key: str
        :param from_source: Whether feature values should be recomputed from the original data source.
            If False, we will read the materialized values from the offline store.
        :type from_source: bool
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: Name to save the DataFrame as. If unspecified and save=True, a name will be generated.
        :type: save_as: str

        Examples:
            An OnDemandFeatureView :py:mod:`fv` that expects request time data for the key :py:mod:`amount`.

            | The request time data is defined in the feature definition as such:
            | `request_schema = StructType()`
            | `request_schema.add(StructField('amount', DoubleType()))`
            | `transaction_request = RequestDataSource(request_schema=request_schema)`

            1) :py:mod:`fv.get_historical_features(spine)` where :py:mod:`spine=pandas.Dataframe({'amount': [30, 50, 10000]})`
            Fetch historical features from the offline store with request time data inputs 30, 50, and 10000 for key 'amount'.

            2) :py:mod:`fv.get_historical_features(spine, save_as='my_dataset')` where :py:mod:`spine=pandas.Dataframe({'amount': [30, 50, 10000]})`
            Fetch historical features from the offline store request time data inputs 30, 50, and 10000 for key 'amount'. Save the DataFrame as dataset with the name 'my_dataset'.

            An OnDemandFeatureView :py:mod:`fv` the expects request time data for the key :py:mod:`amount` and has a feature view dependency with join key :py:mod:`user_id`.

            1) :py:mod:`fv.get_historical_features(spine)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'amount': [30, 50, 10000]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps and values for `amount` in the spine.

        :return: A Tecton :class:`TectonDataFrame`.
        """

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
                append_prefix=False,
            )

        if conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED"):
            if not utils.is_live_workspace(self.workspace):
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE

            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
            )

        return self._get_historical_features(
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=None,
            end_time=None,
            entities=None,
            from_source=from_source,
            save=save,
            save_as=save_as,
        )

    @sdk_public_method
    def get_online_features(
        self,
        join_keys: Optional[Mapping[str, Union[int, np.int_, str, bytes]]] = None,
        include_join_keys_in_response: bool = False,
        request_data: Optional[Mapping[str, Union[int, np.int_, str, bytes, float]]] = None,
    ) -> FeatureVector:
        """
        Returns a single Tecton :class:`tecton.FeatureVector` from the Online Store.
        At least one of join_keys or request_data is required.

        :param join_keys: Join keys of the enclosed FeatureViews.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.
        :param request_data: Dictionary of request context values used for OnDemandFeatureViews.

          Examples:
            An OnDemandFeatureView :py:mod:`fv` that expects request time data for the key :py:mod:`amount`.

            | The request time data is defined in the feature definition as such:
            | `request_schema = StructType()`
            | `request_schema.add(StructField('amount', DoubleType()))`
            | `transaction_request = RequestDataSource(request_schema=request_schema)`

            1) :py:mod:`fv.get_online_features(request_data={'amount': 50})`
            Fetch the latest features with input amount=50.

            An OnDemandFeatureView :py:mod:`fv` that has a feature view dependency with join key :py:mod:`user_id` and expects request time data for the key :py:mod:`amount`.

            1) :py:mod:`fv.get_online_features(join_keys={'user_id': 1}, request_data={'amount': 50}, include_join_keys_in_respone=True)`
            Fetch the latest features from the online store for user 1 with input amount=50.
            In the returned FeatureVector, nclude the join key information (user_id=1).


        :return: A :class:`tecton.FeatureVector` of the results.
        """
        if join_keys is None and request_data is None:
            raise errors.GET_ONLINE_FEATURES_REQUIRED_ARGS
        if join_keys is None and utils.get_num_dependent_fv(self._proto.pipeline.root, visited_inputs={}) > 0:
            raise errors.GET_ONLINE_FEATURES_ODFV_JOIN_KEYS
        if join_keys is not None:
            utils.validate_join_key_types(join_keys)
        if request_data is not None and not isinstance(request_data, dict):
            raise errors.INVALID_REQUEST_DATA_TYPE(type(request_data))

        required_request_context_keys = list(self._request_context.arg_to_schema.keys())
        if len(required_request_context_keys) > 0 and request_data is None:
            raise errors.GET_ONLINE_FEATURES_FV_NO_REQUEST_DATA(required_request_context_keys)
        utils.validate_request_data(request_data, required_request_context_keys)

        return _QueryHelper(self._proto.fco_metadata.workspace, feature_view_name=self.name).get_feature_vector(
            join_keys or {},
            include_join_keys_in_response,
            request_data or {},
            self._request_context,
        )

    @property
    def _request_context(self) -> Optional[_RequestContext]:
        rc = find_request_context(self._proto.pipeline.root)
        return _RequestContext({}) if rc is None else _RequestContext._from_proto(rc)


class StreamFeatureView(FeatureView):
    """
    StreamFeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    @property  # type: ignore
    @sdk_public_method
    def batch_schedule(self) -> Optional[pendulum.Duration]:
        """
        This represents how often we schedule batch materialization jobs.
        """
        return self._batch_materialization_schedule()

    @property  # type: ignore
    @sdk_public_method
    def max_data_delay(self) -> Optional[pendulum.Duration]:
        """
        The maximum data_delay for a data source input to this feature view.

        Tecton will schedule materialization jobs at an offset equal to this. For example, if ``max_data_delay`` is
        one hour, then when materializing the period [Jan 2 00:00:00, Jan 3 00:00:00), Tecton will run the
        materialization job at Jan 3 01:00:00 (instead of at Jan 3 00:00:00).
        """
        return self._schedule_offset()

    @property
    @sdk_public_method
    def timestamp_field(self) -> Optional[str]:
        """
        Returns the timestamp_field of this FeatureView.
        """
        return self._timestamp_key

    @property
    def is_batch_trigger_manual(self):
        """
        Whether batch materialization jobs must be explicitly initiated by the user.
        """
        return self._proto.batch_trigger == BatchTriggerType.BATCH_TRIGGER_TYPE_MANUAL

    @sdk_public_method
    def materialization_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        """
        Displays materialization information for the FeatureView, which may include past jobs, scheduled jobs,
        and job failures. This method returns different information depending on the type of FeatureView.

        :param verbose: If set to true, method will display additional low level materialization information,
            useful for debugging.
        :param limit: Maximum number of jobs to return.
        :param sort_columns: A comma-separated list of column names by which to sort the rows.
        :param: errors_only: If set to true, method will only return jobs that failed with an error.
        """

        return self._materialization_status(verbose, limit, sort_columns, errors_only)

    @sdk_public_method
    def run(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        aggregation_level: str = None,
        **mock_sources: Union[pandas.DataFrame, DataFrame],
    ) -> "tecton.interactive.data_frame.TectonDataFrame":
        """
        Run the FeatureView. Supports transforming data directly from raw data sources or using mock data.

        To run the feature view with data from raw data sources, the environment must have access to the data sources.

        :param start_time: The start time of the time window to materialize. If not set, defaults to `end_time` minus `batch_schedule`. If `end_time` is also not set, defaults to the start of the last complete materialization period.

        :param end_time: The end time of the time window to materialize. If not set, defaults to `start_time` plus `batch_schedule`. If `start_time` is also not set, defaults to the end of the last complete materialization period.

        :param aggregation_level: For feature views with aggregations, `aggregation_level` configures which stage of the aggregation to run up to.

            The query for Aggregate Feature Views operates in three steps:

                1) The feature view query is run over the provided time range. The user defined transformations are applied over the data source.

                2) The result of #1 is aggregated into tiles the size of the aggregation_interval.

                3) The tiles from #2 are combined to form the final feature values. The number of tiles that are combined is based off of the time_window of the aggregation.

            For testing and debugging purposes, to see the output of #1, use ``aggregation_level="disabled"``. For #2, use ``aggregation_level="partial"``. For #3, use ``aggregation_level="full"``.

            ``aggregation_level="full"`` is the default behavior.

        :param \*\*mock_sources: kwargs for mock sources that should be used instead of fetching directly from raw data soruces. The keys should match the feature view's function parameters. For feature views with multiple sources, mocking some data sources and using raw data for others is supported.

        :return: A tecton DataFrame of the results.

        Example:

        .. code-block:: python

            import tecton
            import pandas
            from datetime import datetime

            # Example running a non-aggregate feature view with mock data.
            feature_view = tecton.get_workspace("my_workspace").get_feature_view("my_feature_view")

            mock_fraud_user_data = pandas.DataFrame({
                "user_id": ["user_1", "user_2", "user_3"],
                "timestamp": [datetime(2022, 5, 1, 0), datetime(2022, 5, 1, 2), datetime(2022, 5, 1, 5)],
                "credit_card_number": [1000, 4000, 5000],
            })

            result = feature_view.run(
              start_time=datetime(2022, 5, 1),
              end_time=datetime(2022, 5, 2),
              fraud_users_batch=mock_fraud_user_data)  # `fraud_users_batch` is the name of this FeatureView's data source parameter.

            # Example running an aggregate feature view with real data.
            aggregate_feature_view = tecton.get_workspace("my_workspace").get_feature_view("my_aggregate_feature_view")

            result = aggregate_feature_view.run(
              start_time=datetime(2022, 5, 1),
              end_time=datetime(2022, 5, 2),
              aggregation_level="full")  # or "partial" or "disabled"
        """
        if not self._is_temporal_aggregate and aggregation_level is not None:
            raise errors.FV_UNSUPPORTED_AGGREGATION

        return run_batch(
            self._fd_wrapper(),
            start_time,
            end_time,
            mock_sources,
            FrameworkVersion.FWV5,
            aggregate_tiles=None,
            aggregation_level=aggregation_level,
        )

    @sdk_public_method
    def run_stream(self, output_temp_table: str) -> StreamingQuery:
        """
        Starts a streaming job to keep writting the output records of this FeatureView to a temporary table.
        The job will be running until the execution is terminated.

        After records have been written to the table, they can be queried using `spark.sql()`.
        If ran in a Databricks notebook, Databricks will also automatically visualize the number of incoming records.

        :param output_temp_table: The name of the temporary table to write to.

        Example:

            1) :py:mod:`fv.run_stream(output_temp_table="temp_table")` Start a streaming job.

            2) :py:mod:`display(spark.sql("SELECT * FROM temp_table LIMIT 5"))` Query the output table, and display the output dataframe.
        """
        return run_stream(self._fd_wrapper(), output_temp_table)

    @sdk_public_method
    @is_documented_by(materialization_api.trigger_materialization_job)
    def trigger_materialization_job(
        self,
        start_time: datetime,
        end_time: datetime,
        online: bool,
        offline: bool,
        use_tecton_managed_retries: bool = True,
        overwrite: bool = False,
    ) -> str:
        if not self.is_batch_trigger_manual:
            raise errors.FV_NEEDS_TO_BE_BATCH_TRIGGER_MANUAL(self.name)

        return materialization_api.trigger_materialization_job(
            self.name, self.workspace, start_time, end_time, online, offline, use_tecton_managed_retries, overwrite
        )

    @sdk_public_method
    @is_documented_by(materialization_api.wait_for_materialization_job)
    def wait_for_materialization_job(
        self,
        job_id: str,
        timeout: Optional[timedelta] = None,
    ) -> MaterializationJobData:
        return materialization_api.wait_for_materialization_job(self.name, self.workspace, job_id, timeout)


class BatchFeatureView(FeatureView):
    """
    BatchFeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    @property  # type: ignore
    @sdk_public_method
    @is_documented_by(StreamFeatureView.batch_schedule)
    def batch_schedule(self) -> Optional[pendulum.Duration]:
        return self._batch_materialization_schedule()

    @property  # type: ignore
    @sdk_public_method
    @is_documented_by(StreamFeatureView.max_data_delay)
    def max_data_delay(self) -> Optional[pendulum.Duration]:
        return self._schedule_offset()

    @sdk_public_method
    @is_documented_by(StreamFeatureView.materialization_status)
    def materialization_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        return self._materialization_status(verbose, limit, sort_columns, errors_only)

    @property
    @sdk_public_method
    @is_documented_by(StreamFeatureView.timestamp_field)
    def timestamp_field(self) -> Optional[str]:
        return self._timestamp_key

    @property
    @is_documented_by(StreamFeatureView.is_batch_trigger_manual)
    def is_batch_trigger_manual(self):
        return self._proto.batch_trigger == BatchTriggerType.BATCH_TRIGGER_TYPE_MANUAL

    @sdk_public_method
    @is_documented_by(StreamFeatureView.run)
    def run(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        aggregation_level: str = None,
        **mock_sources: Union[pandas.DataFrame, DataFrame],
    ) -> "tecton.interactive.data_frame.TectonDataFrame":
        if not self._is_temporal_aggregate and aggregation_level is not None:
            raise errors.FV_UNSUPPORTED_AGGREGATION

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.run_batch(
                fd=self._fd_wrapper(),
                feature_start_time=start_time,
                feature_end_time=end_time,
                mock_inputs=mock_sources,
                aggregate_tiles=None,
                aggregation_level=aggregation_level,
            )

        return run_batch(
            self._fd_wrapper(),
            start_time,
            end_time,
            mock_sources,
            FrameworkVersion.FWV5,
            aggregate_tiles=None,
            aggregation_level=aggregation_level,
        )

    @sdk_public_method
    @is_documented_by(materialization_api.trigger_materialization_job)
    def trigger_materialization_job(
        self,
        start_time: datetime,
        end_time: datetime,
        online: bool,
        offline: bool,
        use_tecton_managed_retries: bool = True,
        overwrite: bool = False,
    ) -> str:
        if not self.is_batch_trigger_manual:
            raise errors.FV_NEEDS_TO_BE_BATCH_TRIGGER_MANUAL(self.name)

        return materialization_api.trigger_materialization_job(
            self.name, self.workspace, start_time, end_time, online, offline, use_tecton_managed_retries, overwrite
        )

    @sdk_public_method
    @is_documented_by(materialization_api.wait_for_materialization_job)
    def wait_for_materialization_job(
        self,
        job_id: str,
        timeout: Optional[timedelta] = None,
    ) -> MaterializationJobData:
        return materialization_api.wait_for_materialization_job(self.name, self.workspace, job_id, timeout)


@sdk_public_method
def get_feature_view(fv_reference: str, workspace_name: Optional[str] = None) -> FeatureView:
    """
    Fetch an existing :class:`FeatureView` by name.

    :param fv_reference: Either a name or a hexadecimal Feature View ID.
    :returns: :class:`BatchFeatureView`, :class:`BatchWindowAggregateFeatureView`,
        :class:`StreamFeatureView`, :class:`StreamWindowAggregateFeatureView`,
        or :class:`OnDemandFeatureView`.
    """
    if workspace_name == None:
        logger.warning(
            "`tecton.get_feature_view('<name>')` is deprecated. Please use `tecton.get_workspace('<workspace_name>').get_feature_view('<name>')` instead."
        )

    request = GetFeatureViewRequest()
    request.version_specifier = fv_reference
    request.workspace = workspace_name or conf.get_or_none("TECTON_WORKSPACE")
    request.disable_legacy_response = True
    response = metadata_service.instance().GetFeatureView(request)
    fco_container = FcoContainer(response.fco_container)
    fv_proto = fco_container.get_single_root()

    if not fv_proto:
        raise errors.FCO_NOT_FOUND(FeatureView, fv_reference)

    if fv_proto.HasField("feature_table"):
        raise errors.FCO_NOT_FOUND_WRONG_TYPE(FeatureView, fv_reference, "get_feature_table")

    return get_feature_view_by_type(fv_proto, fco_container)


def get_feature_view_by_type(feature_view_proto: feature_view_pb2.FeatureView, fco_container: FcoContainer):
    assert feature_view_proto.fco_metadata.framework_version == FrameworkVersion.FWV5.value

    if feature_view_proto.HasField("temporal"):
        data_source_type = feature_view_proto.temporal.data_source_type
    if feature_view_proto.HasField("temporal_aggregate"):
        data_source_type = feature_view_proto.temporal_aggregate.data_source_type

    if feature_view_proto.HasField("on_demand_feature_view"):
        return OnDemandFeatureView(feature_view_proto, fco_container)

    if data_source_type == DataSourceType.BATCH:
        return BatchFeatureView(feature_view_proto, fco_container)
    if data_source_type == DataSourceType.STREAM_WITH_BATCH:
        return StreamFeatureView(feature_view_proto, fco_container)

    raise errors.INTERNAL_ERROR("Missing or unsupported FeatureView type.")
