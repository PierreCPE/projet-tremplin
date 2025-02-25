WITH payment_types AS (
    SELECT DISTINCT
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

-- Agréger les données par mois, jour de la semaine et type de paiement
, aggregated_data AS (
    SELECT
        DATE_TRUNC(tpep_pickup_datetime, MONTH) AS month,
        EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) AS day_of_week,
        payment_type,
        COUNT(*) AS trip_count,
        SUM(total_amount) AS total_revenue
    FROM {{ ref('stg_yellow_taxi_agg') }}
    GROUP BY month, day_of_week, payment_type
)

-- Joindre les types de paiements avec les données agrégées
SELECT
    ad.month,
    ad.day_of_week,
    ad.payment_type,
    pt.payment_type_name,
    ad.trip_count,
    ad.total_revenue
FROM aggregated_data AS ad
JOIN payment_types AS pt
ON ad.payment_type = pt.payment_type
ORDER BY ad.month, ad.day_of_week, ad.trip_count DESC