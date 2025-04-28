

with unnested as (
    select
        id::integer as station_id,
        jsonb_array_elements(instruments) as instrument
    from "earth_monitoring"."public"."stg_openaq_location_normalize"
)
select
    (instrument->>'id')::integer as instrument_id,
    instrument->>'name' as name,
    -- If is_monitor exists in your JSON, cast it; otherwise, remove
    (instrument->>'is_monitor')::boolean as is_monitor,
    station_id
from unnested
where (instrument->>'id') is not null