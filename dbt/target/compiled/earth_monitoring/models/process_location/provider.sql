

select distinct
    provider_id,
    provider_name
from "earth_monitoring"."public"."stg_openaq_location_normalize"
where provider_id is not null