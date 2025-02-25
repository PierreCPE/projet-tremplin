-- On veut clean la date car les mois ne sont pas bons 
WITH filtered_data AS (
    SELECT 
        *
    FROM {{ ref('stg_yellow_taxi_agg') }}
    WHERE 
        DATE_TRUNC(tpep_pickup_datetime, MONTH) BETWEEN '2019-01-01' AND '2020-06-30'
        AND DATE_TRUNC(tpep_dropoff_datetime, MONTH) BETWEEN '2019-01-01' AND '2020-06-30'
        AND trip_distance >= 0 AND trip_distance <= 80 AND 
        fare_amount >= 0 AND fare_amount <= 10000 AND
        extra >= 0 AND extra <= 1.5 AND
        tip_amount >= 0 AND tip_amount <= 10000 AND
        tolls_amount >= 0 AND tolls_amount <= 5000 AND
        total_amount >= 0 AND total_amount <= 15000 
        AND
        improvement_surcharge = 0.3

)

SELECT 
    *
FROM filtered_data
