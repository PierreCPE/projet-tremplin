SELECT DISTINCT
    LocationID,
    Borough,
    Zone,
    service_zone
FROM {{ ref('int_yellow_taxi_location') }}
