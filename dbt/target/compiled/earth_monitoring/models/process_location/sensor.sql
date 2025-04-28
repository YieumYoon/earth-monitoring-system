

with unnested as (
    select
        id::integer as station_id,
        jsonb_array_elements(sensors) as sensor
    from "earth_monitoring"."public"."stg_openaq_location_normalize"
)
select
    (sensor->>'id')::integer as sensor_id,
    station_id,
    sensor->>'name' as name,
    (sensor->'parameter'->>'id')::integer as parameter_id
from unnested
where (sensor->>'id') is not null