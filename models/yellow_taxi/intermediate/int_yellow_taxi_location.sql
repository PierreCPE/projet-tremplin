SELECT
    LocationID,
    Borough,
    Zone,
    service_zone
FROM 
    {{ ref('stg_yellow_taxi_location') }}
WHERE Zone != 'NV'
