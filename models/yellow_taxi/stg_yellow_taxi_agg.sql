WITH concatenated_data AS (
    SELECT 
        *,
        CONCAT('2019_01_', CAST(ROW_NUMBER() OVER() AS STRING)) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_01') }}
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

SELECT * 
FROM concatenated_data

