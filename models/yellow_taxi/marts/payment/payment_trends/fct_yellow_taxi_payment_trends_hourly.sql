SELECT 
  EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour_of_day,
  COUNT(*) AS total_trips,
  100 * SUM(CASE WHEN payment_type = 2 THEN 1 ELSE 0 END) / COUNT(*) AS cash_percentage,
  100 * SUM(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END) / COUNT(*) AS card_percentage,
  AVG(fare_amount) AS avg_fare,
  AVG(CASE WHEN payment_type = 1 THEN tip_amount ELSE NULL END) AS avg_tip_card
FROM {{ ref('int_yellow_taxi_agg_cleaned') }}
GROUP BY hour_of_day
ORDER BY hour_of_day
