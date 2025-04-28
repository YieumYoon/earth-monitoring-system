

select distinct
    country_id,
    country_code,
    country_name
from "earth_monitoring"."public"."stg_openaq_location_normalize"
where country_id is not null