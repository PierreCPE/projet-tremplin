{% macro get_payment_type_name(payment_type) %}
    CASE 
        WHEN {{ payment_type }} = 1 THEN 'Credit card'
        WHEN {{ payment_type }} = 2 THEN 'Cash'
        WHEN {{ payment_type }} = 3 THEN 'No charge'
        WHEN {{ payment_type }} = 4 THEN 'Dispute'
        WHEN {{ payment_type }} = 5 THEN 'Unknown'
        ELSE 'Other'
    END
{% endmacro %}

{% macro order_by_weekday(column_name) %}
  CASE 
    WHEN {{ column_name }} = 'Monday' THEN 1
    WHEN {{ column_name }} = 'Tuesday' THEN 2
    WHEN {{ column_name }} = 'Wednesday' THEN 3
    WHEN {{ column_name }} = 'Thursday' THEN 4
    WHEN {{ column_name }} = 'Friday' THEN 5
    WHEN {{ column_name }} = 'Saturday' THEN 6
    WHEN {{ column_name }} = 'Sunday' THEN 7
  END
{% endmacro %}

{% macro adjust_day_of_week(column_name) %}
  CASE 
    WHEN EXTRACT(DAYOFWEEK FROM {{ column_name }}) = 1 THEN 7
    ELSE EXTRACT(DAYOFWEEK FROM {{ column_name }}) - 1
  END
{% endmacro %}


{% macro is_weekend(column_name) %}
  CASE 
    WHEN {{ adjust_day_of_week(column_name) }} IN (6, 7) THEN TRUE 
    ELSE FALSE 
  END
{% endmacro %}