SELECT
    ad.payment_type,
    pt.payment_type_name,
    ad.trip_count,
    ad.total_revenue
FROM {{ ref('stg_yellow_taxi_payment_agg') }} AS ad
JOIN {{ ref('stg_yellow_taxi_payment_type') }} AS pt
ON ad.payment_type = pt.payment_type
ORDER BY ad.trip_count DESC