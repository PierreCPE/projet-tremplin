-- SELECT
--     DATE_TRUNC(tpep_pickup_datetime, MONTH) AS month,
--     EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) AS day_of_week,
--     payment_type,
--     COUNT(*) AS trip_count,
--     SUM(total_amount) AS total_revenue
-- FROM {{ ref('stg_yellow_taxi_agg') }}
-- GROUP BY month, day_of_week, payment_type, tpep_pickup_datetime


SELECT
    DATE_TRUNC(tpep_pickup_datetime, MONTH) AS month,
    COUNT(DATE_TRUNC(tpep_pickup_datetime, MONTH)) as nbr_of_month
    
    -- COUNT(*) AS trip_count,
    -- SUM(total_amount) AS total_revenue
FROM {{ ref('stg_yellow_taxi_agg') }}
GROUP BY month
ORDER by nbr_of_month