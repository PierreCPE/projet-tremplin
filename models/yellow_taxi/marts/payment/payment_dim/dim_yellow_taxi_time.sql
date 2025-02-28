WITH base AS (
    SELECT DISTINCT 
        tpep_pickup_datetime AS date_time
    FROM {{ ref('fct_yellow_taxi_payment_location') }}
)
SELECT 
    date_time, 
    EXTRACT(DATE FROM date_time) AS date,
    {{ adjust_day_of_week('date_time') }} AS jour_semaine, 
    EXTRACT(MONTH FROM date_time) AS mois,
    EXTRACT(HOUR FROM date_time) AS heure,
    {{ is_weekend('date_time') }} AS is_weekend,
    {{ is_holiday('date_time') }} AS is_holiday 
FROM base