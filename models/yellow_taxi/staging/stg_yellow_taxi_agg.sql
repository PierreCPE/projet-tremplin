WITH concatenated_data AS (
    SELECT 
        *,
        CONCAT('2019_01_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ ref('stg_yellow_taxi_2019_01_congestion') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_02_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_02') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_03_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_03') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_04_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_04') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_05_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_05') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_06_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_06') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_07_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_07') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_08_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_08') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_09_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_09') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_10_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_10') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_11_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_11') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2019_12_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_12') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2020_01_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_01') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2020_02_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_02') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2020_03_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_03') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2020_04_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_04') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2020_05_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_05') }}
    UNION ALL
    SELECT 
        *,
        CONCAT('2020_06_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_06') }}
)

SELECT 
    *
FROM concatenated_data
WHERE 
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