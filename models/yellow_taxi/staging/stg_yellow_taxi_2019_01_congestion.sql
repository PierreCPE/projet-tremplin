WITH yellow_tripdata_2019_01_congestion_fix AS (
    SELECT
        VendorID,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        RatecodeID,
        store_and_fwd_flag,
        PULocationID,
        DOLocationID,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        CAST(IFNULL(congestion_surcharge, '0') AS FLOAT64) AS congestion_surcharge
    FROM 
        {{ source('yellow_taxi', 'yellow_tripdata_2019_01') }}
)

SELECT 
    *
FROM yellow_tripdata_2019_01_congestion_fix