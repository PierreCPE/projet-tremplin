SELECT 
  DATE(tpep_pickup_datetime) AS date,
  COUNT(*) AS total_trips,
  SUM(total_amount) AS total_revenue,
  AVG(fare_amount) AS avg_fare,
  100 * SUM(CASE WHEN payment_type = 2 THEN 1 ELSE 0 END) / COUNT(*) AS cash_percentage,
  100 * SUM(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END) / COUNT(*) AS card_percentage,
  AVG(CASE WHEN payment_type = 1 THEN tip_amount ELSE NULL END) AS avg_tip_card
FROM {{ ref('stg_yellow_taxi_agg_cleaned') }}
GROUP BY date
ORDER BY date
