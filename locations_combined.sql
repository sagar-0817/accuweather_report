SELECT
PARSE_TIMESTAMP("%Y-%m-%dT%H:%M:%S%Ez", local_observation_datetime) as observation_datetime_utc, -- Parse the timestamp column
city,
weather_text as weather_type,
has_precipitation,
precipitation_type,
is_day_time,
temperature_celcius,
temperature_fahrenheit
FROM (
  -- Combine data of all 5 cities

  SELECT *,
  "Bengaluru" as city
  FROM `ocean-data-engg.accuweather_data.bengaluru`

  UNION ALL

  SELECT *,
  "Chennai" as city
  FROM `ocean-data-engg.accuweather_data.chennai`

  UNION ALL

  SELECT *,
  "Delhi" as city
  FROM `ocean-data-engg.accuweather_data.delhi`

  UNION ALL

  SELECT *,
  "Mumbai" as city
  FROM `ocean-data-engg.accuweather_data.mumbai`

  UNION ALL

  SELECT *,
  "Kolkata" as city
  FROM `ocean-data-engg.accuweather_data.kolkata`
)
-- Deduplicate the data
QUALIFY ROW_NUMBER() OVER (PARTITION BY local_observation_datetime, city) = 1
