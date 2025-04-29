CREATE SCHEMA IF NOT EXISTS processed;

DROP TABLE IF EXISTS processed.daily_seoul_weather;

CREATE TABLE processed.daily_seoul_weather AS
SELECT
    DATE(datetime) AS date,
    AVG(tempmax) AS tempmax,
    AVG(tempmin) AS tempmin,
    AVG(temp) AS temp,
    AVG(humidity) AS humidity,
    AVG(precip) AS precip,
    AVG(precipprob) AS precipprob,
    AVG(precipcover) AS precipcover,
    AVG(preciptype) ASpreciptype,
    AVG(snow) AS snow,
    AVG(snowdepth) AS snowdepth,
    AVG(windgust) AS windgust,
    AVG(windspeed) AS windspeed,
    AVG(winddir) AS winddir,
    AVG(sealevelpressure) AS sealevelpressure,
    AVG(cloudcover) AS cloudcover,
    AVG(visibility) AS visibility,
    AVG(solarradiation) AS solarradiation,
    AVG(solarenergy) AS solarenergy,
    AVG(uvindex) AS uvindex,
    AVG(severerisk) AS severerisk,
    MIN(sunrise) AS sunrise,
    MAX(sunset) AS sunset,
    conditions,
    description,
    icon
FROM raw.seoul_weather_2016_2019
GROUP BY DATE(datetime)
ORDER BY DATE(datetime);

-- Add unique constraint on date after table creation
ALTER TABLE processed.daily_seoul_weather
ADD CONSTRAINT uq_daily_weather_date UNIQUE (date);