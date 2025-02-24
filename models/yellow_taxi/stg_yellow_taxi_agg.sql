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
    
)

SELECT * 
FROM concatenated_data