SELECT
    payment_type,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue
FROM {{ ref('stg_yellow_taxi_agg') }}
GROUP BY payment_type