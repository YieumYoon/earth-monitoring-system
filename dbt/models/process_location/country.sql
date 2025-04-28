{{ config(materialized='incremental', unique_key='country_id') }}

select distinct
    country_id,
    country_code,
    country_name
from {{ ref('stg_openaq_location_normalize') }}
where country_id is not null