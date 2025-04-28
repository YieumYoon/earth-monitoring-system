-- Create schema for our environmental data
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS processed;

-- Create table for air quality data matching OpenAQ API response columns exactly
CREATE TABLE IF NOT EXISTS raw.air_quality (
    id SERIAL PRIMARY KEY,
    name TEXT,
    locality TEXT,
    timezone TEXT,
    is_mobile BOOLEAN,
    is_monitor BOOLEAN,
    instruments JSONB,
    sensors JSONB,
    bounds JSONB,
    distance FLOAT,
    datetime_first TEXT,
    datetime_last TEXT,
    country_id INTEGER,
    country_code TEXT,
    country_name TEXT,
    owner_id INTEGER,
    owner_name TEXT,
    provider_id INTEGER,
    provider_name TEXT,
    latitude FLOAT,
    longitude FLOAT,
    datetime_first_utc TEXT,
    datetime_first_local TEXT,
    datetime_last_utc TEXT,
    datetime_last_local TEXT
);
