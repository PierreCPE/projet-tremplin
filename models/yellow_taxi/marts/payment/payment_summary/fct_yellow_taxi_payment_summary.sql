{% set payment_type_name = get_payment_type_name('payment_type') %}

SELECT 
  payment_type, 
  {{ payment_type_name }} AS payment_type_name,
  COUNT(*) AS total_trips, 
  SUM(total_amount + CASE WHEN payment_type = 1 THEN tip_amount ELSE 0 END) AS total_revenue_with_tips,
  SUM(total_amount) AS total_revenue_without_tips,
  AVG(total_amount + CASE WHEN payment_type = 1 THEN tip_amount ELSE 0 END) AS avg_fare_with_tips,
  AVG(total_amount) AS avg_fare_without_tips
FROM {{ ref('stg_yellow_taxi_agg_cleaned') }}
GROUP BY payment_type
ORDER BY total_revenue_with_tips DESC