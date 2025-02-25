WITH filtered_data AS (
    SELECT 
        *
    FROM {{ ref('stg_yellow_taxi_agg') }}
    WHERE 
        DATE_TRUNC(tpep_pickup_datetime, MONTH) BETWEEN '2019-01-01' AND '2020-06-30'
        AND DATE_TRUNC(tpep_dropoff_datetime, MONTH) BETWEEN '2019-01-01' AND '2020-06-30'
)

SELECT 
    *
FROM filtered_data