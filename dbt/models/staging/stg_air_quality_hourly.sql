-- In your dbt/models/staging/stg_air_quality_hourly.sql
WITH source AS (
    SELECT
        id,
        location_id,
        sensor_id,
        parameter,
        value,
        unit,
        timestamp,
        fetched_at
    FROM raw.air_quality_hourly
)

SELECT
    id,
    location_id,
    sensor_id,
    parameter,
    value,
    unit,
    timestamp,
    DATE(timestamp) AS date,
    EXTRACT(HOUR FROM timestamp) AS hour
FROM source