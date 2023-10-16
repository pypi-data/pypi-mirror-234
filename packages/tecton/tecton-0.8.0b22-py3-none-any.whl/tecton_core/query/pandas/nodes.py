import logging
import os
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pandas
import pendulum

from tecton_core import conf
from tecton_core import feature_set_config
from tecton_core import specs
from tecton_core.data_types import BoolType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_core.data_types import TimestampType
from tecton_core.duckdb_context import DuckDBContext
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.filter_context import FilterContext
from tecton_core.id_helper import IdHelper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.pandas import pipeline_helper
from tecton_core.query.pandas.node import PandasExecNode
from tecton_core.query.pandas.node import SqlExecNode
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.pipeline_pb2 import TransformationNode
from tecton_proto.args.transformation_pb2 import TransformationMode
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.data.batch_data_source_pb2 import FileDataSourceFormat


logger = logging.getLogger(__name__)

# Maps a tecton datatype to the correct pandas datatype which is to be used when an output schema is defined by the user
PRIMITIVE_TECTON_DATA_TYPE_TO_PANDAS_DATA_TYPE = {
    Int32Type(): "int32",
    Int64Type(): "int64",
    Float32Type(): "float32",
    Float64Type(): "float64",
    StringType(): "string",
    BoolType(): "bool",
    TimestampType(): "datetime64[ns]",
}


@attrs.frozen
class PandasDataSourceScanNode(PandasExecNode):
    ds: specs.DataSourceSpec
    ds_node: Optional[DataSourceNode]
    is_stream: bool = attrs.field()
    start_time: Optional[datetime]
    end_time: Optional[datetime]

    def _to_dataframe(self) -> pandas.DataFrame:
        if self.ds.type not in (DataSourceType.STREAM_WITH_BATCH, DataSourceType.BATCH, DataSourceType.PUSH_WITH_BATCH):
            msg = "Only batch and streaming data sources supported (non-Ingest API)"
            raise Exception(msg)

        batch_source = self.ds.batch_source
        assert batch_source
        if isinstance(batch_source, specs.SparkBatchSourceSpec):
            msg = "Pandas mode does not support a data source function yet"
            raise Exception(msg)
        elif isinstance(batch_source, specs.PandasBatchSourceSpec):
            df = self._get_ds_from_dsf(batch_source)
        elif (
            isinstance(batch_source, specs.FileSourceSpec)
            and batch_source.file_format == FileDataSourceFormat.FILE_DATA_SOURCE_FORMAT_PARQUET
        ):
            df = self._get_df_from_parquet(batch_source)
        else:
            msg = "Pandas mode only supports parquet batch data sources"
            raise Exception(msg)

        if self.ds.type == DataSourceType.STREAM_WITH_BATCH:
            schema = self.ds.stream_source.spark_schema
            cols = [field.name for field in schema.fields]
            df = df[cols]
        elif self.ds.type == DataSourceType.PUSH_WITH_BATCH:
            schema = self.ds.schema.tecton_schema
            cols = [field.name for field in schema.columns]
            df = df[cols]
        return df

    def _get_ds_from_dsf(self, batch_source: specs.PandasBatchSourceSpec) -> pandas.DataFrame:
        if batch_source.supports_time_filtering:
            filter_context = FilterContext(self.start_time, self.end_time)
            return batch_source.function(filter_context)
        return batch_source.function()

    def _get_df_from_parquet(self, batch_source: specs.FileSourceSpec) -> pandas.DataFrame:
        # TODO(danny): support other file formats and schema overrides
        file_uri = batch_source.uri
        source = self.ds.batch_source
        timestamp_field = source.timestamp_field
        from tecton_core.query.query_tree_compute import DuckDBCompute

        duckdb_compute = DuckDBCompute(session=DuckDBContext.get_instance().get_connection())
        s3_prefix_sql = ""
        if file_uri.startswith("s3://"):
            # TODO(danny): consider making this a conf
            if "AWS_REGION" in os.environ:
                s3_region = os.environ["AWS_REGION"]
            else:
                s3_region = "us-west-2"
            s3_prefix_sql = f"""
                LOAD httpfs;
                SET s3_region='{s3_region}';
                SET s3_access_key_id='{conf.get_or_none("AWS_ACCESS_KEY_ID")}';
                SET s3_secret_access_key='{conf.get_or_none("AWS_SECRET_ACCESS_KEY")}';
                """

        scan_sql = (
            s3_prefix_sql
            + f"""
            SELECT *
            FROM read_parquet('{file_uri}')
        """
        )
        where_conditions = []
        if self.start_time:
            where_conditions.append(f"{timestamp_field} >= CAST('{self.start_time}' AS TIMESTAMP)")
        if self.end_time:
            where_conditions.append(f"{timestamp_field} < CAST('{self.end_time}' AS TIMESTAMP)")
        if len(where_conditions) > 0:
            scan_sql += f"WHERE {' AND '.join(where_conditions)}"
        df = duckdb_compute.run_sql(scan_sql, return_dataframe=True).to_pandas()

        return df


@attrs.frozen
class PandasFeatureViewPipelineNode(PandasExecNode):
    inputs_map: Dict[str, NodeRef]
    feature_definition_wrapper: FeatureDefinitionWrapper
    feature_time_limits: Optional[pendulum.Period]

    def _to_dataframe(self):
        df = self._node_to_value(self.feature_definition_wrapper.pipeline.root)
        return df

    def _node_to_value(self, pipeline_node: PipelineNode) -> pandas.DataFrame:
        if pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_dataframe(pipeline_node.transformation_node)
        elif pipeline_node.HasField("data_source_node"):
            ds_query_node = self.inputs_map[pipeline_node.data_source_node.input_name].node
            return PandasDataSourceScanNode.from_node_inputs(query_node=ds_query_node, input_node=None).to_dataframe()

    def _transformation_node_to_dataframe(self, transformation_node: TransformationNode) -> pandas.DataFrame:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args: List[Union[pandas.DataFrame, str, int, float, bool]] = []
        kwargs = {}
        id_to_transformation = {t.id: t for t in self.feature_definition_wrapper.transformations}
        transformation = id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function
        for transformation_input in transformation_node.inputs:
            node_value = self._node_to_value(transformation_input.node)
            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                msg = f"Unknown argument type for Input node: {transformation_input}"
                raise KeyError(msg)

        return user_function(*args, **kwargs)


@attrs.frozen
class PandasStagedTableScanNode(PandasExecNode):
    input_df: pandas.DataFrame

    def _to_dataframe(self) -> pandas.DataFrame:
        return self.input_df

    def to_dataframe(self) -> pandas.DataFrame:
        # Ignore the super class check since this is a pass-through
        return self._to_dataframe()


@attrs.frozen
class PandasMultiOdfvPipelineNode(PandasExecNode):
    input_node: Union[PandasExecNode, SqlExecNode]
    feature_definition_wrappers_namespaces: List[Tuple[FeatureDefinitionWrapper, str]]
    use_namespace_feature_prefix: bool

    def _to_dataframe(self):
        output_df = self.input_node._to_dataframe()
        # Apply each ODFV sequentially. Note that attempting to apply ODFV
        # udfs in parallel as we traverse data rows does not meaningfully
        # speed up execution on Athena (unlike in Spark).
        for fdw, namespace in self.feature_definition_wrappers_namespaces:
            output_df = self._get_odfv_output_df(output_df, fdw, namespace)
        return output_df

    def _get_odfv_output_df(
        self, input_df: pandas.DataFrame, fdw: FeatureDefinitionWrapper, namespace: str
    ) -> pandas.DataFrame:
        odfv_result_df = self._run_odfv(input_df, fdw)
        rename_map = {}
        datatypes = {}
        # Namespace ODFV outputs to this FV to avoid conflicts in output schemas
        # with other FV
        output_schema = fdw.view_schema.column_name_and_data_types()
        for column_name, datatype in output_schema:
            if self.use_namespace_feature_prefix:
                mapped_name = self.column_name_updater(f"{namespace}{fdw.namespace_separator}{column_name}")
            else:
                mapped_name = column_name
            rename_map[column_name] = mapped_name
            if datatype in PRIMITIVE_TECTON_DATA_TYPE_TO_PANDAS_DATA_TYPE:
                datatypes[mapped_name] = PRIMITIVE_TECTON_DATA_TYPE_TO_PANDAS_DATA_TYPE[datatype]
        odfv_result_df = odfv_result_df.rename(columns=rename_map)[[*rename_map.values()]].astype(datatypes)
        data_df = input_df.merge(odfv_result_df, left_index=True, right_index=True)
        return data_df

    def _run_odfv(self, data_df: pandas.DataFrame, odfv: FeatureDefinitionWrapper) -> pandas.DataFrame:
        transformation_mode = odfv.transformations[0].transformation_mode

        odfv_pipeline = pipeline_helper.build_odfv_execution_pipeline(
            pipeline=odfv.pipeline, transformations=odfv.transformations, name=odfv.name
        )

        odfv_transformation_node = odfv.pipeline.root.transformation_node
        odfv_inputs = self._extract_inputs_for_odfv_from_data(
            transformation_node=odfv_transformation_node, data_df=data_df, odfv_invocation_inputs={}, odfv=odfv
        )

        if transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
            odfv_result_df = odfv_pipeline.execute_with_inputs(odfv_inputs)
            return odfv_result_df
        elif transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
            # The inputs are currently a mapping of input_name to pandas DF
            # We need turn the ODFV inputs from a pandas DF to a list of dictionaries
            # Then we need to iterate through all rows of the input data set, pass the input dicts into the ODFV
            # And finally convert the resulting list of dicts into a pandas DF
            for input_name in odfv_inputs.keys():
                # Map pandas DFs to List of dicts (one dict per row)
                odfv_inputs[input_name] = odfv_inputs[input_name].to_dict("records")

            odfv_result_list = []

            num_rows = len(data_df)
            if num_rows > 100:
                logger.warn(
                    f"Executing ODFV {odfv.name} for {len(data_df)} rows. The ODFV will be executed row by row and may take a while to complete..."
                )

            for row_index in range(num_rows):
                # Iterate through all rows of the data and invoke the ODFV
                row_odfv_inputs = {}
                for input_name in odfv_inputs.keys():
                    row_odfv_inputs[input_name] = odfv_inputs[input_name][row_index]

                odfv_result_dict = odfv_pipeline.execute_with_inputs(row_odfv_inputs)
                odfv_result_list.append(odfv_result_dict)
            return pandas.DataFrame.from_dict(odfv_result_list)
        else:
            msg = f"ODFV {odfv.name} has an unexpected transformation mode: {transformation_mode}"
            raise TectonValidationError(msg)

    def _extract_inputs_for_odfv_from_data(
        self,
        transformation_node: TransformationNode,
        data_df: pandas.DataFrame,
        odfv_invocation_inputs: Dict[str, pandas.DataFrame],
        odfv: FeatureDefinitionWrapper,
    ) -> Dict[str, pandas.DataFrame]:
        for input in transformation_node.inputs:
            if input.node.HasField("request_data_source_node"):
                input_name = input.node.request_data_source_node.input_name
                request_context_schema = input.node.request_data_source_node.request_context.tecton_schema
                request_context_fields = [self.column_name_updater(c.name) for c in request_context_schema.columns]

                for f in request_context_fields:
                    if f not in data_df.columns:
                        msg = f"ODFV {odfv.name} has a dependency on the Request Data Source named '{input_name}'. Field {f} of this Request Data Source is not found in the spine. Available columns: {list(data_df.columns)}"
                        raise TectonValidationError(msg)

                input_df = data_df[request_context_fields]
                odfv_invocation_inputs[input_name] = input_df
            elif input.node.HasField("feature_view_node"):
                input_name = input.node.feature_view_node.input_name
                fv_features = feature_set_config.find_dependent_feature_set_items(
                    odfv.fco_container, input.node, {}, odfv.id
                )[0]
                # Generate dependent column mappings since dependent FV have
                # internal column names with _udf_internal
                select_columns_and_rename_map = {}
                for f in fv_features.features:
                    column_name = self.column_name_updater(f"{fv_features.namespace}__{f}")
                    mapped_name = self.column_name_updater(f)
                    select_columns_and_rename_map[column_name] = mapped_name
                for f in select_columns_and_rename_map.keys():
                    if f not in data_df.columns:
                        msg = f"ODFV {odfv.name} has a dependency on the Feature View '{input_name}'. Feature {f} of this Feature View is not found in the retrieved historical data. Available columns: {list(data_df.columns)}"
                        raise TectonValidationError(msg)
                # Let's select all of the features of the input FV from data_df
                input_df = data_df.rename(columns=select_columns_and_rename_map)[
                    [*select_columns_and_rename_map.values()]
                ]
                odfv_invocation_inputs[input_name] = input_df
            elif input.node.HasField("transformation_node"):
                self._extract_inputs_for_odfv_from_data(
                    transformation_node=input.node.transformation_node,
                    data_df=data_df,
                    odfv_invocation_inputs=odfv_invocation_inputs,
                    odfv=odfv,
                )
            else:
                msg = f"Unexpected input found ({input.arg_name}) on ODFV {odfv.name}"
                raise Exception(msg)
        return odfv_invocation_inputs


@attrs.frozen
class PandasRenameColsNode(PandasExecNode):
    input_node: Union[PandasExecNode, SqlExecNode]
    mapping: Optional[Dict[str, str]]
    drop: Optional[List[str]]

    def _to_dataframe(self) -> pandas.DataFrame:
        input_df = self.input_node._to_dataframe()
        output_df = input_df
        if self.drop:
            columns_to_drop = [self.column_name_updater(name) for name in self.drop]
            output_df = input_df.drop(columns=columns_to_drop)
        if self.mapping:
            output_df = input_df.rename(self.mapping)
        return output_df
