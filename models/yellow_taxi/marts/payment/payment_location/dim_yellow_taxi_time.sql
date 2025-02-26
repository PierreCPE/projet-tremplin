WITH base AS (
    SELECT DISTINCT 
        tpep_pickup_datetime AS date_time
    FROM {{ ref('stg_yellow_taxi_agg_cleaned') }}
)
SELECT 
    date_time, 
    EXTRACT(DATE FROM date_time) AS date,
    EXTRACT(DAYOFWEEK FROM date_time) AS jour_semaine,  -- 1 = Dimanche, 7 = Samedi --> faut que je le change ca je pense pour garder la logique de semaine de la macros, a voir comment utiliser la macros
    EXTRACT(MONTH FROM date_time) AS mois,
    EXTRACT(HOUR FROM date_time) AS heure,
    CASE WHEN EXTRACT(DAYOFWEEK FROM date_time) IN (1, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM base
