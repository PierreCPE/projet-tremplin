WITH yellow_tripdata_2019_01_congestion_fix AS (
    SELECT,
        CAST(IFNULL(congestion_surcharge, '0') AS FLOAT64) AS congestion_surcharge
    FROM 
        {{ source('yellow_taxi', 'yellow_tripdata_2019_01') }}
)

SELECT 
    *
FROM yellow_tripdata_2019_01_congestion_fix
