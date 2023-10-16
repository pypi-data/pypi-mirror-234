{% macro copy_into(destination, source, materialization_schema, cast_types) %}
COPY INTO {{ destination }}
FROM (
    SELECT
        {%- for column in materialization_schema.columns %}
            {%- if column.feature_server_data_type.type == data_type_pb2.DATA_TYPE_ARRAY and column.feature_server_data_type.array_element_type.type == data_type_pb2.DATA_TYPE_STRING %}
                TO_ARRAY({{ column.name }},'string') AS {{ column.name }}
            {%- elif cast_types[column.feature_server_type] != None %}
                {{ column.name }}::{{ cast_types[column.feature_server_type] }} AS {{ column.name }}
            {%- else %}
                {{ column.name }}
            {%- endif %}
            {%- if not loop.last %}, {%- endif %}
        {%- endfor %}
    FROM ({{ source }})
)
header = true
detailed_output = true
file_format = (type=parquet)
{% endmacro %}
