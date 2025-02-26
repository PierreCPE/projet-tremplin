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