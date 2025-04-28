-- Create schema for our environmental data
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS processed;

-- Create table for air quality data matching OpenAQ API response columns exactly
CREATE TABLE IF NOT EXISTS raw.openaq_location (
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


-- Main Station Table   
CREATE TABLE IF NOT EXISTS processed.station (
    station_id INTEGER PRIMARY KEY,
    name TEXT,
    latitude FLOAT,
    longitude FLOAT,
    timezone_id INTEGER REFERENCES processed.timezone(timezone_id),
    country_id INTEGER REFERENCES processed.country(country_id),
    provider_id INTEGER REFERENCES processed.provider(provider_id),
    owner_id INTEGER REFERENCES processed.owner(owner_id),
    instrument_id INTEGER REFERENCES processed.instrument(instrument_id),
    -- datetime_first_utc TIMESTAMPTZ,
    -- datetime_first_local TIMESTAMPTZ,
    -- datetime_last_utc TIMESTAMPTZ,
    -- datetime_last_local TIMESTAMPTZ
);

-- Country Table
CREATE TABLE IF NOT EXISTS processed.country (
    country_id INTEGER PRIMARY KEY,
    country_code TEXT,
    country_name TEXT
);

-- Provider Table
CREATE TABLE IF NOT EXISTS processed.provider (
    provider_id INTEGER PRIMARY KEY,
    name TEXT
);

-- Timezone Table
CREATE TABLE IF NOT EXISTS processed.timezone (
    timezone_id INTEGER PRIMARY KEY,
    name TEXT
);

-- Sensor Table
CREATE TABLE IF NOT EXISTS processed.sensor (
    sensor_id INTEGER PRIMARY KEY,
    station_id INTEGER REFERENCES processed.station(station_id),
    name TEXT,
    parameter_id INTEGER REFERENCES processed.parameter(parameter_id)
);

-- Parameter Table 
CREATE TABLE IF NOT EXISTS processed.parameter (
    parameter_id INTEGER PRIMARY KEY,
    name TEXT,
    units TEXT,
    display_name TEXT
);

-- Instrument Table
CREATE TABLE IF NOT EXISTS processed.instrument (
    instrument_id INTEGER PRIMARY KEY,
    name TEXT
    is_monitor BOOLEAN
);

-- Owner Table
CREATE TABLE IF NOT EXISTS processed.owner (
    owner_id INTEGER PRIMARY KEY,
    name TEXT
);
