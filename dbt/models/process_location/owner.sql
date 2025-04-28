{{ config(materialized='incremental', unique_key='owner_id') }}

select distinct
    owner_id,
    owner_name
from {{ ref('stg_openaq_location_normalize') }}
where owner_id is not null