
      
        
            delete from "earth_monitoring"."public"."sensor"
            where (
                sensor_id) in (
                select (sensor_id)
                from "sensor__dbt_tmp214802903820"
            );

        
    

    insert into "earth_monitoring"."public"."sensor" ("sensor_id", "station_id", "name", "parameter_id")
    (
        select "sensor_id", "station_id", "name", "parameter_id"
        from "sensor__dbt_tmp214802903820"
    )
  