from tecton_core import aggregation_utils
from tecton_core import data_types as tecton_types
from tecton_core import errors
from tecton_core import query_consts
from tecton_proto.args import feature_view_pb2
from tecton_proto.common import schema_pb2


def _get_feature_server_data_type(offline_data_type: tecton_types.DataType) -> tecton_types.DataType:
    if offline_data_type == tecton_types.Int32Type():
        return tecton_types.Int64Type()
    return offline_data_type


def column_from_tecton_data_type(offline_data_type: tecton_types.DataType) -> schema_pb2.Column:
    return schema_pb2.Column(
        offline_data_type=offline_data_type.proto,
        feature_server_data_type=_get_feature_server_data_type(offline_data_type).proto,
    )


def _get_timestamp_field(feature_view_args: feature_view_pb2.FeatureViewArgs, view_schema: schema_pb2.Schema) -> str:
    timestamp_key = ""

    if feature_view_args.materialized_feature_view_args.HasField("timestamp_field"):
        timestamp_key = feature_view_args.materialized_feature_view_args.timestamp_field
    else:
        timestamp_fields = [
            column for column in view_schema.columns if column.offline_data_type == tecton_types.TimestampType().proto
        ]

        if len(timestamp_fields) != 1:
            msg = "The timestamp_field must be set on the Feature View or the feature view transformation output should contain only one and only one column of type Timestamp"
            raise errors.TectonValidationError(msg)
        timestamp_key = timestamp_fields[0].name

    view_schema_column_names = [column.name for column in view_schema.columns]
    if timestamp_key not in view_schema_column_names:
        msg = f"Timestamp key '{timestamp_key}' not found in view schema. View schema has columns: {', '.join(view_schema_column_names)}"
        raise errors.TectonValidationError(msg)
    return timestamp_key


def populate_schema_with_derived_fields(schema: schema_pb2.Schema) -> None:
    """Copies the behavior of populateSchemaWithDerivedFields in FeatureViewUtils.kt.

    Should only be applied to the schemas of Push Sources, which are expected to have the offline_data_type field set.
    """
    for column in schema.columns:
        assert column.offline_data_type is not None
        tecton_types.data_type_from_proto(column.offline_data_type)
        column.feature_server_data_type.CopyFrom(column.offline_data_type)


def compute_aggregate_materialization_schema_from_view_schema(
    view_schema: schema_pb2.Schema,
    feature_view_args: feature_view_pb2.FeatureViewArgs,
    is_spark: bool,
) -> schema_pb2.Schema:
    materialization_schema_columns = []
    view_schema_column_map = {column.name: column for column in view_schema.columns}

    # Add join key columns from view schema to materializaton schema.
    join_keys = []
    for entity in feature_view_args.entities:
        join_keys.extend(entity.join_keys)
    for join_key in join_keys:
        if join_key not in view_schema_column_map:
            msg = f"Join key {join_key} not found in view schema. View schema has columns {','.join(view_schema_column_map.keys())}"
            raise errors.TectonValidationError(msg)
        materialization_schema_columns.append(view_schema_column_map[join_key])

    # Add columns for aggregate features.
    added = []
    for aggregation in feature_view_args.materialized_feature_view_args.aggregations:
        if aggregation.column not in view_schema_column_map:
            msg = f"Column {aggregation.column} used for aggregations not found in view schema. View schema has columns {','.join(view_schema_column_map.keys())}"
            raise errors.TectonValidationError(msg)
        input_column = view_schema_column_map[aggregation.column]

        is_continuous = (
            feature_view_args.materialized_feature_view_args.stream_processing_mode
            == feature_view_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
        )
        prefixes = aggregation_utils.get_materialization_aggregation_column_prefixes(
            aggregation_utils.get_aggregation_enum_from_string(aggregation.function.lower()),
            aggregation.function_params,
            is_continuous,
        )
        for prefix in prefixes:
            materialization_column_name = aggregation_utils.get_materialization_column_name(prefix, input_column.name)

            tecton_type = aggregation_utils.aggregation_prefix_to_tecton_type(prefix)
            if tecton_type is None:
                tecton_type = tecton_types.data_type_from_proto(input_column.offline_data_type)

            column_proto = schema_pb2.Column()
            column_proto.CopyFrom(column_from_tecton_data_type(tecton_type))
            column_proto.name = materialization_column_name

            if materialization_column_name not in added:
                materialization_schema_columns.append(column_proto)
                added.append(materialization_column_name)

    # Add column for timestamp. For Spark, aggregate feature views use an anchor time column.
    if is_spark:
        column_proto = schema_pb2.Column()
        column_proto.CopyFrom(column_from_tecton_data_type(tecton_types.Int32Type()))
        column_proto.name = query_consts.ANCHOR_TIME
        materialization_schema_columns.append(column_proto)
    else:
        timestamp_key = _get_timestamp_field(feature_view_args, view_schema)
        materialization_schema_columns.append(view_schema_column_map[timestamp_key])

    return schema_pb2.Schema(columns=materialization_schema_columns)
