from base64 import b64encode
from typing import List
from typing import Union

import pandas as pd
from pyspark import sql as pyspark_sql
from pyspark.sql import functions as pyspark_functions
from pyspark.sql import types as pyspark_types

from tecton import tecton_context
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import spark_api
from tecton._internals import utils
from tecton_core import feature_definition_wrapper
from tecton_core import id_helper
from tecton_proto.common import fco_locator_pb2
from tecton_proto.common import id_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.online_store import feature_value_pb2
from tecton_spark import ingest_utils


def delete_keys(
    online: bool,
    offline: bool,
    keys: Union[pyspark_sql.DataFrame, pd.DataFrame],
    feature_definition: feature_definition_wrapper.FeatureDefinitionWrapper,
):
    if not offline and not online:
        raise errors.NO_STORE_SELECTED

    materialization_state_transitions = feature_definition.fv_spec.materialization_state_transitions
    if offline and any([transition.offline_enabled for transition in materialization_state_transitions]):
        if not feature_definition.offline_store_config.HasField("delta"):
            raise errors.OFFLINE_STORE_NOT_SUPPORTED

    if online and all([not transition.online_enabled for transition in materialization_state_transitions]):
        print("Online materialization was never enabled. No data to be deleted in online store.")
        online = False

    if offline and all([not transition.offline_enabled for transition in materialization_state_transitions]):
        print("Offline materialization was never enabled. No data to be deleted in offline store.")
        offline = False

    if not (offline or online):
        return None

    spark_df = _get_keys_spark_df(keys, feature_definition.view_schema)
    utils.validate_entity_deletion_keys_dataframe(
        df=spark_df, join_keys=feature_definition.join_keys, view_schema=feature_definition.view_schema
    )

    info_response = _get_delete_entities_info(feature_definition.id)
    s3_path = info_response.df_path
    offline_join_keys_path = s3_path + "/offline"
    online_join_keys_path = s3_path + "/online"
    if online:
        _write_to_online_join_keys_path(online_join_keys_path, keys, feature_definition.join_keys)
    if offline:
        spark_api.write_dataframe_to_path_or_url(
            keys, offline_join_keys_path, info_response.signed_url_for_df_upload_offline, feature_definition.view_schema
        )

    _send_deletion_request(feature_definition, online, offline, online_join_keys_path, offline_join_keys_path)
    return None


def _send_deletion_request(
    feature_definition: feature_definition_wrapper.FeatureDefinitionWrapper,
    online: bool,
    offline: bool,
    online_join_keys_path: str,
    offline_join_keys_path: str,
):
    deletion_request = metadata_service_pb2.DeleteEntitiesRequest(
        fco_locator=fco_locator_pb2.FcoLocator(
            id=id_helper.IdHelper.from_string(feature_definition.id), workspace=feature_definition.workspace
        ),
        online=online,
        offline=offline,
        online_join_keys_path=online_join_keys_path,
        offline_join_keys_path=offline_join_keys_path,
    )
    metadata_service.instance().DeleteEntities(deletion_request)
    print(
        "A deletion job has been created. You can track the status of the job in the Web UI under Materialization section or with deletion_status(). The deletion jobs have a type 'Deletion'."
    )


def _get_delete_entities_info(id_proto: id_pb2.Id) -> metadata_service_pb2.GetDeleteEntitiesInfoResponse:
    info_request = metadata_service_pb2.GetDeleteEntitiesInfoRequest(
        feature_definition_id=id_helper.IdHelper.from_string(id_proto),
    )
    return metadata_service.instance().GetDeleteEntitiesInfo(info_request)


def _get_keys_spark_df(keys: Union[pyspark_sql.DataFrame, pd.DataFrame], view_schema) -> pyspark_sql.DataFrame:
    if isinstance(keys, pd.DataFrame):
        if len(keys) == 0:
            raise errors.EMPTY_ARGUMENT("join_keys")
        if len(keys.columns[keys.columns.duplicated()]):
            raise errors.DUPLICATED_COLS_IN_KEYS(", ".join(list(keys.columns)))
        return ingest_utils.convert_pandas_to_spark_df(keys, view_schema)
    elif isinstance(keys, pyspark_sql.DataFrame):
        return keys
    else:
        raise errors.INVALID_JOIN_KEY_TYPE(type(keys))


def _write_to_online_join_keys_path(
    online_join_keys_path: str, keys: Union[pyspark_sql.DataFrame, pd.DataFrame], join_keys: List[str]
):
    # We actually generate the presigned url but it's not used for online case
    spark = tecton_context.TectonContext.get_instance()._spark
    if isinstance(keys, pd.DataFrame):
        spark_keys_df = spark.createDataFrame(keys)
    else:
        spark_keys_df = keys
    spark_keys_df = spark_keys_df.distinct()
    join_key_df = _serialize_join_keys(spark_keys_df, join_keys)

    # coalesce(1) causes it to write to 1 file, but the jvm code
    # is actually robust to multiple files here
    join_key_df.coalesce(1).write.csv(online_join_keys_path)


def _serialize_join_keys(spark_keys_df: pyspark_sql.DataFrame, join_keys: List[str]):
    def serialize_fn(x):
        ret = feature_value_pb2.FeatureValueList()
        for item in x:
            if isinstance(item, int):
                ret.feature_values.add().int64_value = item
            elif isinstance(item, str):
                ret.feature_values.add().string_value = item
            elif item is None:
                ret.feature_values.add().null_value.CopyFrom(feature_value_pb2.NullValue())
            else:
                raise Exception(f"Unknown type: {type(item)}")
        return b64encode(ret.SerializeToString()).decode()

    serialize = pyspark_functions.udf(serialize_fn, pyspark_types.StringType())
    return spark_keys_df.select(pyspark_functions.struct(*join_keys).alias("join_keys_array")).select(
        serialize("join_keys_array")
    )
