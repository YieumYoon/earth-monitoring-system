-- Stage air quality data, performing basic cleaning and formatting
WITH source AS (
    SELECT
        id,
        location_id,
        city,
        country,
        latitude,
        longitude,
        parameter,
        value,
        unit,
        timestamp,
        source_name,
        geom
    FROM raw.air_quality
)

SELECT
    id,
    location_id,
    COALESCE(city, 'Unknown') AS city,
    COALESCE(country, 'Unknown') AS country,
    latitude,
    longitude,
    parameter,
    value,
    unit,
    timestamp,
    source_name,
    geom,
    DATE(timestamp) AS date
FROM source
