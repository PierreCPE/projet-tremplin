SELECT
    SUM(CASE WHEN trip_id IS NULL THEN 1 ELSE 0 END) AS trip_id_null_count,
    SUM(CASE WHEN VendorID IS NULL THEN 1 ELSE 0 END) AS VendorID_null_count,
    SUM(CASE WHEN tpep_pickup_datetime IS NULL THEN 1 ELSE 0 END) AS tpep_pickup_datetime_null_count,
    SUM(CASE WHEN tpep_dropoff_datetime IS NULL THEN 1 ELSE 0 END) AS tpep_dropoff_datetime_null_count,
    SUM(CASE WHEN passenger_count IS NULL THEN 1 ELSE 0 END) AS passenger_count_null_count,
    SUM(CASE WHEN trip_distance IS NULL THEN 1 ELSE 0 END) AS trip_distance_null_count,
    SUM(CASE WHEN RatecodeID IS NULL THEN 1 ELSE 0 END) AS RatecodeID_null_count,
    SUM(CASE WHEN store_and_fwd_flag IS NULL THEN 1 ELSE 0 END) AS store_and_fwd_flag_null_count,
    SUM(CASE WHEN PULocationID IS NULL THEN 1 ELSE 0 END) AS PULocationID_null_count,
    SUM(CASE WHEN DOLocationID IS NULL THEN 1 ELSE 0 END) AS DOLocationID_null_count,
    SUM(CASE WHEN payment_type IS NULL THEN 1 ELSE 0 END) AS payment_type_null_count,
    SUM(CASE WHEN fare_amount IS NULL THEN 1 ELSE 0 END) AS fare_amount_null_count,
    SUM(CASE WHEN extra IS NULL THEN 1 ELSE 0 END) AS extra_null_count,
    SUM(CASE WHEN mta_tax IS NULL THEN 1 ELSE 0 END) AS mta_tax_null_count,
    SUM(CASE WHEN tip_amount IS NULL THEN 1 ELSE 0 END) AS tip_amount_null_count,
    SUM(CASE WHEN tolls_amount IS NULL THEN 1 ELSE 0 END) AS tolls_amount_null_count,
    SUM(CASE WHEN improvement_surcharge IS NULL THEN 1 ELSE 0 END) AS improvement_surcharge_null_count,
    SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END) AS total_amount_null_count,
    SUM(CASE WHEN congestion_surcharge IS NULL THEN 1 ELSE 0 END) AS congestion_surcharge_null_count
FROM {{ ref('stg_yellow_taxi_agg') }}

-- Pour la premiere itération que l'on a eu :
-- On a environ 500 000 valeures nulles sur 100 000 000 ce qui est négligeable si elles sont toutes sur les meme lignes (donc 500 000 lignes en moins) on va vérif : 
-- Pour la deuxieme ( un fois le code de dessous executé) nous avons bien 0 valeurs nulles en tout dans la table aggrégé



-- SELECT
--     trip_id,
--     VendorID,
--     tpep_pickup_datetime,
--     tpep_dropoff_datetime,
--     passenger_count,
--     trip_distance,
--     RatecodeID,
--     store_and_fwd_flag,
--     PULocationID,
--     DOLocationID,
--     payment_type,
--     fare_amount,
--     extra,
--     mta_tax,
--     tip_amount,
--     tolls_amount,
--     improvement_surcharge,
--     total_amount,
--     congestion_surcharge,
--     (CASE WHEN VendorID IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN tpep_pickup_datetime IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN tpep_dropoff_datetime IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN passenger_count IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN trip_distance IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN RatecodeID IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN store_and_fwd_flag IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN PULocationID IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN DOLocationID IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN payment_type IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN fare_amount IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN extra IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN mta_tax IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN tip_amount IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN tolls_amount IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN improvement_surcharge IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END +
--      CASE WHEN congestion_surcharge IS NULL THEN 1 ELSE 0 END) AS null_count
-- FROM {{ ref('stg_yellow_taxi_agg') }}
-- WHERE (VendorID IS NULL OR
--        tpep_pickup_datetime IS NULL OR
--        tpep_dropoff_datetime IS NULL OR
--        passenger_count IS NULL OR
--        trip_distance IS NULL OR
--        RatecodeID IS NULL OR
--        store_and_fwd_flag IS NULL OR
--        PULocationID IS NULL OR
--        DOLocationID IS NULL OR
--        payment_type IS NULL OR
--        fare_amount IS NULL OR
--        extra IS NULL OR
--        mta_tax IS NULL OR
--        tip_amount IS NULL OR
--        tolls_amount IS NULL OR
--        improvement_surcharge IS NULL OR
--        total_amount IS NULL OR
--        congestion_surcharge IS NULL)
-- ORDER BY null_count DESC


-- On se rend compte que les valeures nulles sont sur la meme ligne donc on va les enlever lors de la concaténation des tables sources