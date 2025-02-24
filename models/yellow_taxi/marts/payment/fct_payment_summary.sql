WITH payment_types AS (
    SELECT
        payment_type,
        CASE 
            WHEN payment_type = 1 THEN 'Credit card'
            WHEN payment_type = 2 THEN 'Cash'
            WHEN payment_type = 3 THEN 'No charge'
            WHEN payment_type = 4 THEN 'Dispute'
            WHEN payment_type = 5 THEN 'Unknown'
            ELSE 'Other'
        END AS payment_type_name
    FROM {{ ref('stg_yellow_taxi_agg') }}
)

SELECT
    pt.payment_type,
    pt.payment_type_name,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue
FROM {{ ref('stg_yellow_taxi_agg') }} AS stg
JOIN payment_types AS pt
ON stg.payment_type = pt.payment_type
GROUP BY pt.payment_type, pt.payment_type_name
-- ORDER BY trip_count DESC