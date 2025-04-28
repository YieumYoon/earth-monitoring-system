
      
        
            delete from "earth_monitoring"."public"."instrument"
            where (
                instrument_id) in (
                select (instrument_id)
                from "instrument__dbt_tmp214802494178"
            );

        
    

    insert into "earth_monitoring"."public"."instrument" ("instrument_id", "name", "is_monitor", "station_id")
    (
        select "instrument_id", "name", "is_monitor", "station_id"
        from "instrument__dbt_tmp214802494178"
    )
  