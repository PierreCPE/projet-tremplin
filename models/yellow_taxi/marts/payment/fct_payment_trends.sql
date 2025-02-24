SELECT
    DATE_TRUNC(tpep_pickup_datetime, MONTH) AS month,
    payment_type,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue
FROM {{ ref('stg_yellow_taxi_agg') }}
GROUP BY month, payment_type
ORDER BY month, payment_type