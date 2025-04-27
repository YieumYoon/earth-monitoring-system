-- Create schema for our environmental data
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS processed;

-- Create tables for air quality data
CREATE TABLE IF NOT EXISTS raw.air_quality (
    id SERIAL PRIMARY KEY,
    location_id TEXT,
    city TEXT,
    country TEXT,
    latitude FLOAT,
    longitude FLOAT,
    parameter TEXT,
    value FLOAT,
    unit TEXT,
    timestamp TIMESTAMP,
    source_name TEXT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Add geometry column for spatial analysis
SELECT AddGeometryColumn('raw', 'air_quality', 'geom', 4326, 'POINT', 2);

-- Create index for spatial queries
CREATE INDEX air_quality_geom_idx ON raw.air_quality USING GIST(geom);

-- Create trigger to automatically update the geometry column
CREATE OR REPLACE FUNCTION update_geom_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.geom := ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_air_quality_geom
BEFORE INSERT OR UPDATE ON raw.air_quality
FOR EACH ROW EXECUTE PROCEDURE update_geom_column();
