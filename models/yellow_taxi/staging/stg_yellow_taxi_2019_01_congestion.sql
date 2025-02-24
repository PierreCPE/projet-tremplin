with 
yellow_tripdata_2019_01_congestion_fix

as (
select
CAST(IFNULL(congestion_surcharge, '0') AS congestion_surcharge

from 
{{ source('yellow_taxi', 'yellow_tripdata_2019_01') }}
)

SELECT 
    congestion_surcharge,
    COUNT(*) AS count
FROM yellow_tripdata_2019_01_congestion_fix
GROUP BY congestion_surcharge
ORDER BY count DESC