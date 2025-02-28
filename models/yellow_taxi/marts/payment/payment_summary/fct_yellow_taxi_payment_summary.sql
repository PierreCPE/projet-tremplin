{% set payment_type_name = get_payment_type_name('payment_type') %}

SELECT 
  payment_type, 
  {{ payment_type_name }} AS payment_type_name,
  COUNT(*) AS total_trips, 
  SUM(total_amount) AS total_revenue_with_tips,
  SUM(total_amount - tip_amount) AS total_revenue_without_tips,
  AVG(total_amount) AS avg_fare_with_tips,
  AVG(total_amount - tip_amount) AS avg_fare_without_tips
FROM {{ ref('int_yellow_taxi_agg_cleaned') }}
GROUP BY payment_type
ORDER BY total_revenue_with_tips DESC