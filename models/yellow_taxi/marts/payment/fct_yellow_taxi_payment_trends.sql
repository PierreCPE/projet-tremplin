{% set payment_type_name = get_payment_type_name('payment_type') %}

SELECT
    payment_type,
    {{ payment_type_name }} AS payment_type_name,
    DATE_TRUNC(tpep_pickup_datetime, MONTH) AS month,
    EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) AS day_of_week,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue

FROM {{ ref('stg_yellow_taxi_agg') }}

GROUP BY 
   
    month,
    payment_type, payment_type_name,
    day_of_week
