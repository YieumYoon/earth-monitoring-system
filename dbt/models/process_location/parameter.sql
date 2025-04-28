{{ config(materialized='incremental', unique_key='parameter_id') }}

with unnested as (
    select
        jsonb_array_elements(sensors) as sensor
    from {{ ref('stg_openaq_location_normalize') }}
)
select distinct
    (sensor->'parameter'->>'id')::integer as parameter_id,
    sensor->'parameter'->>'name' as name,
    sensor->'parameter'->>'units' as units,
    sensor->'parameter'->>'display_name' as display_name
from unnested
where (sensor->'parameter'->>'id') is not null