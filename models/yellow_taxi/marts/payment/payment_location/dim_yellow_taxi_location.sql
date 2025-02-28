WITH stg_temp_location AS (
    SELECT
        LocationID,
        Borough,
        Zone,
        service_zone
    FROM 
        {{ ref('stg_yellow_taxi_location') }}
)

SELECT 
    fct.PULocationID,
    stg_temp_location.*
FROM 
    {{ ref('fct_yellow_taxi_payment_location') }} AS fct
LEFT JOIN 
    stg_temp_location
    ON fct.PULocationID = stg_temp_location.LocationID
