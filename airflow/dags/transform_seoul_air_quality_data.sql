CREATE SCHEMA IF NOT EXISTS processed;

DROP TABLE IF EXISTS processed.daily_seoul_air_quality;

CREATE TABLE processed.daily_seoul_air_quality AS
SELECT
    DATE(measurement_date) AS date,
    ROUND(AVG(pm10)) AS avg_pm10,
    ROUND(AVG(pm25)) AS avg_pm25,
    ROUND(AVG(o3), 3) AS avg_o3,
    ROUND(AVG(no2), 3) AS avg_no2,
    ROUND(AVG(co), 1) AS avg_co,
    ROUND(AVG(so2), 3) AS avg_so2
FROM raw.seoul_air_quality_2017_2019
GROUP BY DATE(measurement_date)
ORDER BY DATE(measurement_date);

-- Add unique constraint on date after table creation
ALTER TABLE processed.daily_seoul_air_quality
ADD CONSTRAINT uq_daily_aq_date UNIQUE (date);