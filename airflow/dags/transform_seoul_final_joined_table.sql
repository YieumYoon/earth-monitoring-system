CREATE SCHEMA IF NOT EXISTS processed;

DROP TABLE IF EXISTS processed.daily_seoul_air_quality_weather;

CREATE TABLE processed.daily_seoul_air_quality_weather AS
SELECT
    w.date,
    aq.avg_pm10,
    aq.avg_pm25,
    aq.avg_o3,
    aq.avg_no2,
    aq.avg_co,
    aq.avg_so2,
    w.tempmax,
    w.tempmin,
    w.temp,
    w.humidity,
    w.precip,
    w.precipprob,
    w.precipcover,
    w.snow,
    w.snowdepth,
    w.windgust,
    w.windspeed,
    w.winddir,
    w.sealevelpressure,
    w.cloudcover,
    w.visibility,
    w.solarradiation,
    w.solarenergy,
    w.uvindex,
    w.severerisk,
    w.sunrise,
    w.sunset,
    w.conditions,
    w.description,
    w.icon
FROM processed.daily_seoul_weather w
LEFT JOIN processed.daily_seoul_air_quality aq
    ON w.date = aq.date
ORDER BY w.date;

-- Add unique constraint on date
ALTER TABLE processed.daily_seoul_air_quality_weather
ADD CONSTRAINT uq_daily_joined_date UNIQUE (date);
