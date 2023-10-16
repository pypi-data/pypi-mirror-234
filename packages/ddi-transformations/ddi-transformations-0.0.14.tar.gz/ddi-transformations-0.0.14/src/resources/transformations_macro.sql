{% set ns = namespace(transformed_value='') %}

{% set ns1 = namespace(transformation_types = {
    'Remove Special Characters': "REGEXP_REPLACE(column_name,'[^a-zA-Z0-9 ]','')",
    'Trim Spaces': "REPLACE(column_name,'')",
    'Lower Case': "LOWER(column_name)",
    'Upper Case': "UPPER(column_name)",
    'Add Prefix': "CONCAT(value, column_name)",
    'Add Suffix': "CONCAT(column_name, value)",
    'Replace Values': "REPLACE(column_name, value1, value2)",
    'Replace Index': "REPLACE(column_name, SUBSTR(column_name,value),'')",
    'Absolute': "ABS(column_name)",
    'Round Off': "ROUND(column_name, value)",
    'Change Date Format': "TO_DATE(column_name)",
    'Truncate': "SUBSTR(column_name, value1, value2)",
    'Right': "RIGHT(column_name, LEN(column_name)-value)",
    'Left': "LEFT(column_name, LEN(column_name)-value)",
    'Split by Characters': "TO_VARCHAR(SPLIT(column_name, value))",
    'Fill Blanks': "COALESCE(NULLIF(column_name,''), value)"
    })
%}

{% set function_name = transform_details['functionName'] %}
{% set function_type = transform_details['type'] %}
{% set ns.transformed_value = ns1.transformation_types[function_name] ~ ' AS "' ~ column_name ~ '"' %}
{% set ns.transformed_value = ns.transformed_value.replace('column_name', column_name) %}

{% if function_type == 'TEXT' and function_name == 'Round Off' %}
    {% set function_input = transform_details['value'] %}
    {% set ns.transformed_value = ns.transformed_value.replace('value', function_input) %}
{% elif function_type == 'TEXT' %}
    {% set function_input = transform_details['value'] %}
    {% set ns.transformed_value = ns.transformed_value.replace('value', add_quotes(function_input)) %}
{% elif function_type == 'RANGE' %}
    {% set function_input = transform_details['value'] %}
    {% set value1 = (function_input|string).split(':')[0] %}
    {% set value2 = (function_input|string).split(':')[1] %}
    {% set ns.transformed_value = ns.transformed_value.replace('value1', add_quotes(value1)) %}
    {% set ns.transformed_value = ns.transformed_value.replace('value2', add_quotes(value2)) %}
{% endif %}

{{ return(ns.transformed_value) }}