{%- set join_key_list = join_keys|join(", ")  %}
WITH _SOURCE_WITH_TILE_TIME AS (
    SELECT
        DATEADD('SECOND', -MOD(DATE_PART(EPOCH_SECOND, {{ timestamp_key }}), {{ slide_interval.ToSeconds() }}), DATE_TRUNC('SECOND', {{ timestamp_key }})) AS _TILE_TIMESTAMP_KEY,
        {%- for column, functions in aggregations.items() -%}
            {%- for prefix, snowflake_function in functions %}
                {%- if snowflake_function == "ROW_NUMBER" %}
                    ROW_NUMBER() OVER (PARTITION BY {{ join_key_list }},_TILE_TIMESTAMP_KEY order by {{timestamp_key}} desc) AS ROW_NUMBER_OF_{{ column }},
                {%- endif -%}
            {%- endfor -%}
        {%- endfor -%}
        *
	FROM ({{ source }})
)
SELECT
    {{ join_key_list }},
    {%- for column, functions in aggregations.items() -%}
        {%- for prefix, snowflake_function in functions %}
    	    {%- if prefix == "SUM_OF_SQUARES" %}
                SUM(SQUARE(CAST({{ column }} AS float))) AS {{ prefix }}_{{ column }},
            {%- elif prefix.startswith("LAST_NON_DISTINCT_N") %}
                {# Last non-distinct aggregation now uses "snowflake_function" field to hold the n param. #}
                {# TODO(TEC-10982): Refactor the aggregation struct passed into this template so function param can be handled appropriately. #}
                ARRAYAGG(CASE WHEN ROW_NUMBER_OF_{{ column }} <= {{ snowflake_function }} THEN {{ column }} END) WITHIN GROUP (ORDER BY ROW_NUMBER_OF_{{ column }} DESC) AS {{ prefix }}_{{ column }},
            {%- elif prefix != "ROW_NUMBER" %}
                {{ snowflake_function }}({{ column }}) AS {{ prefix }}_{{ column }},
            {%- endif %}
        {%- endfor %}
    {%- endfor %}
    _TILE_TIMESTAMP_KEY as {{ timestamp_key }}
FROM (
    _SOURCE_WITH_TILE_TIME
)
GROUP BY {{ join_key_list }}, _TILE_TIMESTAMP_KEY
