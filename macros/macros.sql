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

{% macro is_holiday(date_column) %}
    CASE
        WHEN EXTRACT(DATE FROM {{ date_column }}) IN (
            '2019-01-01', '2019-01-21', '2019-02-18', '2019-05-27', '2019-07-04', '2019-09-02', '2019-10-14', '2019-11-11', '2019-11-28', '2019-12-25',
            '2020-01-01', '2020-01-20', '2020-02-17', '2020-05-25'
        ) THEN TRUE
        ELSE FALSE
    END
{% endmacro %}