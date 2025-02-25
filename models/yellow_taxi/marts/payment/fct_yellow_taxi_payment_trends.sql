SELECT
    payment_type,
    CASE 
        WHEN payment_type = 1 THEN 'Credit card'
        WHEN payment_type = 2 THEN 'Cash'
        WHEN payment_type = 3 THEN 'No charge'
        WHEN payment_type = 4 THEN 'Dispute'
        WHEN payment_type = 5 THEN 'Unknown'
        ELSE 'Other'
    END AS payment_type_name,
    DATE_TRUNC(tpep_pickup_datetime, MONTH) AS month,
    EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) AS day_of_week,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue

FROM {{ ref('stg_yellow_taxi_agg') }}

GROUP BY 
   
    month,
    payment_type, payment_type_name,
    day_of_week

-- ORDER BY 
--     month, 
--     day_of_week, 
--     trip_count 