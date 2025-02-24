-- On morcele car sinon trop gourmand
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

-- Agréger les données par type de paiement
-- , aggregated_data AS (
--     SELECT
--         payment_type,
--         COUNT(*) AS trip_count,
--         SUM(total_amount) AS total_revenue
--     FROM {{ ref('stg_yellow_taxi_agg') }}
--     GROUP BY payment_type
-- )

-- Jointure les types de paiements avec les données agrégées
-- SELECT
--     ad.payment_type,
--     pt.payment_type_name,
--     ad.trip_count,
--     ad.total_revenue
-- FROM aggregated_data AS ad
-- JOIN payment_types AS pt
-- ON ad.payment_type = pt.payment_type
-- ORDER BY ad.trip_count DESC

select * 
from payment_types