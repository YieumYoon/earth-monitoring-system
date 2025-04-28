

select distinct
    owner_id,
    owner_name
from "earth_monitoring"."public"."stg_openaq_location_normalize"
where owner_id is not null