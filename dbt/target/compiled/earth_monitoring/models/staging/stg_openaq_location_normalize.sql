-- dbt/models/staging/stg_openaq_location_normalize.sql

with raw as (
    select
        *
    from "earth_monitoring"."raw"."openaq_location"
)

select
    id,
    name,
    locality,
    timezone,
    is_mobile,
    is_monitor,
    instruments,
    sensors,
    bounds,
    distance,
    datetime_first,
    datetime_last,
    country_id,
    country_code,
    country_name,
    owner_id,
    owner_name,
    provider_id,
    provider_name,
    latitude,
    longitude,
    datetime_first_utc,
    datetime_first_local,
    datetime_last_utc,
    datetime_last_local
from raw