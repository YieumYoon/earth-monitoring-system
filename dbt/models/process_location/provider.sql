{{ config(materialized='incremental', unique_key='provider_id') }}

select distinct
    provider_id,
    provider_name
from {{ ref('stg_openaq_location_normalize') }}
where provider_id is not null