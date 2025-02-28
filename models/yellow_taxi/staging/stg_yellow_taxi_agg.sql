WITH concatenated_data AS (
    SELECT 
        *,
        CAST(CONCAT('201901', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ ref('stg_yellow_taxi_2019_01_congestion') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201902', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_02') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201903', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_03') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201904', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_04') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201905', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_05') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201906', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_06') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201907', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_07') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201908', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_08') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201909', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_09') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201910', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_10') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201911', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_11') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('201912', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2019_12') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('202001', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_01') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('202002', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_02') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('202003', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_03') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('202004', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_04') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('202005', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_05') }}
    UNION ALL
    SELECT 
        *,
        CAST(CONCAT('202006', ROW_NUMBER() OVER() ) AS INT) AS trip_id
    FROM {{ source('yellow_taxi', 'yellow_tripdata_2020_06') }}
)

SELECT 
    *
FROM concatenated_data
