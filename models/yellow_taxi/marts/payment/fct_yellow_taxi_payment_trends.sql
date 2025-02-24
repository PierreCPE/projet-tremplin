SELECT
    ad.month,
    ad.day_of_week,
    ad.payment_type,
    pt.payment_type_name,
    ad.trip_count,
    ad.total_revenue
FROM {{ ref('stg_yellow_taxi_payment_trends') }} AS ad
JOIN {{ ref('stg_yellow_taxi_payment_type') }} AS pt
ON ad.payment_type = pt.payment_type
-- ORDER BY ad.month, ad.day_of_week, ad.trip_count DESC