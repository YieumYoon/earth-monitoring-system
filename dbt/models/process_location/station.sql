{{ config(materialized='incremental', unique_key='station_id') }}

select
    id::integer as station_id,
    name,
    locality,
    timezone,
    latitude,
    longitude,
    null as timezone_id,
    country_id,
    provider_id,
    owner_id,
    null as instrument_id  -- To be filled if instrument logic is added
from {{ ref('stg_openaq_location_normalize') }}