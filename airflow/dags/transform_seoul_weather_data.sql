-- Transformation for daily seoul weather
CREATE SCHEMA IF NOT EXISTS processed;

DROP TABLE IF EXISTS processed.daily_seoul_weather;

CREATE TABLE processed.daily_seoul_weather AS
SELECT
    DATE(datetime) AS date,
    tempmax,
    tempmin,
    temp,
    feelslikemax,
    feelslikemin,
    feelslike,
    dew,
    humidity,
    precip,
    precipprob,
    precipcover,
    preciptype,
    snow,
    snowdepth,
    windgust,
    windspeed,
    winddir,
    sealevelpressure,
    cloudcover,
    visibility,
    solarradiation,
    solarenergy,
    uvindex,
    severerisk,
    sunrise,
    sunset,
    moonphase,
    conditions,
    description,
    icon
FROM raw.seoul_weather_2017_2019
ORDER BY DATE(datetime);

ALTER TABLE processed.daily_seoul_weather
ADD CONSTRAINT uq_daily_weather_date UNIQUE (date);