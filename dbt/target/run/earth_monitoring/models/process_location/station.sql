
      
        
            delete from "earth_monitoring"."public"."station"
            where (
                station_id) in (
                select (station_id)
                from "station__dbt_tmp214802896905"
            );

        
    

    insert into "earth_monitoring"."public"."station" ("station_id", "name", "locality", "timezone", "latitude", "longitude", "timezone_id", "country_id", "provider_id", "owner_id", "instrument_id")
    (
        select "station_id", "name", "locality", "timezone", "latitude", "longitude", "timezone_id", "country_id", "provider_id", "owner_id", "instrument_id"
        from "station__dbt_tmp214802896905"
    )
  