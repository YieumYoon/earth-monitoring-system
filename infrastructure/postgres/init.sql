-- Create schema for our environmental data
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS processed;

DROP TABLE IF EXISTS raw.seoul_air_quality_2017_2019;
DROP TABLE IF EXISTS raw.seoul_weather_2017_2019;

--2017-2019
CREATE TABLE raw.seoul_air_quality_2017_2019 (
    measurement_date TIMESTAMP,
    station_code VARCHAR(10),
    address TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    so2 DOUBLE PRECISION,
    no2 DOUBLE PRECISION,
    o3 DOUBLE PRECISION,
    co DOUBLE PRECISION,
    pm10 DOUBLE PRECISION,
    pm25 DOUBLE PRECISION
);

CREATE TABLE raw.seoul_weather_2017_2019 (
    name TEXT,
    datetime TIMESTAMP,
    tempmax DOUBLE PRECISION,
    tempmin DOUBLE PRECISION,
    temp DOUBLE PRECISION,
    feelslikemax DOUBLE PRECISION,
    feelslikemin DOUBLE PRECISION,
    feelslike DOUBLE PRECISION,
    dew DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    precip DOUBLE PRECISION,
    precipprob DOUBLE PRECISION,
    precipcover DOUBLE PRECISION,
    preciptype TEXT,
    snow DOUBLE PRECISION,
    snowdepth DOUBLE PRECISION,
    windgust DOUBLE PRECISION,
    windspeed DOUBLE PRECISION,
    winddir DOUBLE PRECISION,
    sealevelpressure DOUBLE PRECISION,
    cloudcover DOUBLE PRECISION,
    visibility DOUBLE PRECISION,
    solarradiation DOUBLE PRECISION,
    solarenergy DOUBLE PRECISION,
    uvindex DOUBLE PRECISION,
    severerisk DOUBLE PRECISION,
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    moonphase DOUBLE PRECISION,
    conditions TEXT,
    description TEXT,
    icon TEXT,
    stations TEXT
);
