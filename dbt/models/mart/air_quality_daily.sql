-- In dbt/models/mart/air_quality_daily.sql
WITH hourly_data AS (
    SELECT
        date,
        location_id,
        parameter,
        AVG(value) as avg_value,
        MAX(value) as max_value,
        MIN(value) as min_value,
        COUNT(*) as measurement_count
    FROM {{ ref('stg_air_quality_hourly') }}
    GROUP BY date, location_id, parameter
),

location_info AS (
    SELECT DISTINCT
        location_id,
        city,
        country,
        latitude,
        longitude
    FROM {{ ref('stg_air_quality') }}
)

SELECT
    h.date,
    h.location_id,
    l.city,
    l.country,
    l.latitude,
    l.longitude,
    h.parameter,
    h.avg_value,
    h.max_value,
    h.min_value,
    h.measurement_count
FROM hourly_data h
LEFT JOIN location_info l
    ON h.location_id = l.location_id