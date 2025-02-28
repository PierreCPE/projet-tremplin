SELECT
LocationID,
Borough,
Zone,
service_zone
FROM 
{{ source('yellow_taxi', 'taxi_zone_lookup') }}