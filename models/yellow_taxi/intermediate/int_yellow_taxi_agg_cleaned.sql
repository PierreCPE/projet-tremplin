WITH filtered_data AS (
    SELECT 
        *
    FROM {{ ref('stg_yellow_taxi_agg') }}
    WHERE 
        VendorID IN (1, 2)
        AND tpep_pickup_datetime BETWEEN '2019-01-01' AND '2020-06-30'
        AND tpep_dropoff_datetime BETWEEN '2019-01-01' AND '2020-06-30'
        AND Trip_distance > 0 AND Trip_distance <= 80
        AND PULocationID BETWEEN 1 AND 265
        AND DOLocationID BETWEEN 1 AND 265
        AND RateCodeID BETWEEN 1 AND 6
        AND Payment_type BETWEEN 1 AND 5
        AND Fare_amount BETWEEN 0 AND 100
        AND Extra IN (0.50, 1)
        AND MTA_tax = 0.50
        AND Tip_amount BETWEEN 0 AND 1000
        AND Tolls_amount BETWEEN 0 AND 1000
        AND Total_amount > 0 AND Total_amount < 10000
        AND
        improvement_surcharge = 0.3
        AND TIMESTAMP_DIFF(tpep_dropoff_datetime, tpep_pickup_datetime, HOUR) < 30
        AND
        trip_id IS NOT NULL AND
        VendorID IS NOT NULL AND
        tpep_pickup_datetime IS NOT NULL AND
        tpep_dropoff_datetime IS NOT NULL AND
        passenger_count IS NOT NULL AND
        trip_distance IS NOT NULL AND
        RatecodeID IS NOT NULL AND
        store_and_fwd_flag IS NOT NULL AND
        PULocationID IS NOT NULL AND
        DOLocationID IS NOT NULL AND
        payment_type IS NOT NULL AND
        fare_amount IS NOT NULL AND
        extra IS NOT NULL AND
        mta_tax IS NOT NULL AND
        tip_amount IS NOT NULL AND
        tolls_amount IS NOT NULL AND
        improvement_surcharge IS NOT NULL AND
        total_amount IS NOT NULL AND
        congestion_surcharge IS NOT NULL
)

SELECT 
    *
FROM filtered_data
