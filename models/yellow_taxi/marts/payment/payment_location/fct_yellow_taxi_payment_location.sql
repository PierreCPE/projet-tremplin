-- {{ config(materialized='table') }}

SELECT 
    tpep_pickup_datetime, 
    tpep_dropoff_datetime,
    PULocationID, 
    DOLocationID, 
    trip_distance, 
    fare_amount, 
    tip_amount, 
    total_amount, 
    payment_type
    
FROM {{ ref('stg_yellow_taxi_agg_cleaned') }}
