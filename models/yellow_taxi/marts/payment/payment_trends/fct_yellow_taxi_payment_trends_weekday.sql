SELECT 
  FORMAT_TIMESTAMP('%A', tpep_pickup_datetime) AS weekday,
  COUNT(*) AS total_trips,
  100 * SUM(CASE WHEN payment_type = 2 THEN 1 ELSE 0 END) / COUNT(*) AS cash_percentage,
  100 * SUM(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END) / COUNT(*) AS card_percentage,
  AVG(fare_amount) AS avg_fare,
  AVG(CASE WHEN payment_type = 1 THEN tip_amount ELSE NULL END) AS avg_tip_card
FROM {{ ref('stg_yellow_taxi_agg_cleaned') }}
GROUP BY weekday
ORDER BY {{ order_by_weekday('weekday') }}