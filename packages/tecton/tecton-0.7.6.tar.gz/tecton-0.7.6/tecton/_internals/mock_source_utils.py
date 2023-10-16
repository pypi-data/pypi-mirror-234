from typing import Any
from typing import Dict
from typing import List
from typing import Union

import pandas
from pyspark.sql import DataFrame

from tecton._internals import errors
from tecton.framework import data_frame
from tecton_core import pipeline_common
from tecton_core import specs
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import UserSpecifiedDataNode


def convert_mock_inputs_to_mock_sources(
    fdw: FeatureDefinitionWrapper, mock_inputs: Dict[str, Union[pandas.DataFrame, DataFrame]]
) -> Dict[str, NodeRef]:
    validate_batch_mock_inputs(mock_inputs, fdw)

    input_ds_id_map = pipeline_common.get_input_name_to_ds_id_map(fdw.pipeline)

    mock_data_sources = {
        input_ds_id_map[key]: NodeRef(UserSpecifiedDataNode(data_frame.TectonDataFrame._create(mock_inputs[key])))
        for key in mock_inputs.keys()
    }
    return mock_data_sources


def validate_batch_mock_inputs(mock_inputs: Dict[str, Union[pandas.DataFrame, DataFrame]], fd: FeatureDefinition):
    """Validate the mock data source data used for `run()` and `test_run()`.

    This validation does not enforce that the mock data schema is exactly equivalent to the data source schema, however
    it does check for schemas that will usually lead to a bad downstream error.

    For example, it is okay if the mock data is missing some fields (the fields may not be used/needed in the feature
    view transformation), but it's not okay if the mock data is missing the `timestamp_field` defined in the data
    source, since that is used by Tecton time filtering.
    """
    # Validate that mock_inputs keys are a subset of data sources.
    expected_input_names = [
        node.data_source_node.input_name for node in pipeline_common.get_all_data_source_nodes(fd.pipeline)
    ]
    mock_inputs_keys = set(mock_inputs.keys())
    if not mock_inputs_keys.issubset(expected_input_names):
        raise errors.FV_INVALID_MOCK_INPUTS(list(mock_inputs_keys), expected_input_names)

    # Validate some required fields in the mock data schemas.
    for key, mock_df in mock_inputs.items():
        data_source = fd.get_data_source_with_input_name(key)
        if data_source.batch_source is None:
            msg = f"Data Source '{data_source.name}' does not have a batch config and cannot be used with mock data."
            raise TectonValidationError(msg)

        column_names = get_pandas_or_spark_df_or_dict_columns(mock_df)

        if (
            data_source.batch_source.timestamp_field is not None
            and data_source.batch_source.timestamp_field not in column_names
        ):
            msg = f"Data Source '{data_source.name}' specified a timestamp_field '{data_source.batch_source.timestamp_field}', but that timestamp field was not found in the mock data source columns: '{column_names}'"
            raise TectonValidationError(msg)

        if isinstance(data_source.batch_source, specs.HiveSourceSpec):
            for datetime_partition_column in data_source.batch_source.datetime_partition_columns:
                if datetime_partition_column.column_name not in column_names:
                    msg = f"Data Source '{data_source.name}' specified a datetime partition column '{datetime_partition_column.column_name}', but that column was not found in the mock data source schema: '{column_names}'"
                    raise errors.TectonValidationError(msg)


def get_pandas_or_spark_df_or_dict_columns(df: Union[pandas.DataFrame, DataFrame, Dict[str, Any]]) -> List[str]:
    if isinstance(df, pandas.DataFrame):
        return list(df.columns)
    elif isinstance(df, DataFrame):
        return [field.name for field in df.schema.fields]
    elif isinstance(df, dict):
        return list(df.keys())
    else:
        msg = f"Unexpected mock data type '{type(df)}'. Should be a Pandas or Spark data frame or Python dictionary."
        raise TypeError(msg)
