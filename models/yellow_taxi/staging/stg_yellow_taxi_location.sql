SELECT * FROM {{ source('yellow_taxi', 'taxi_zone_lookup') }}
