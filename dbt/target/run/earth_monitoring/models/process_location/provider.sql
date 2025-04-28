
      
        
            delete from "earth_monitoring"."public"."provider"
            where (
                provider_id) in (
                select (provider_id)
                from "provider__dbt_tmp214802852614"
            );

        
    

    insert into "earth_monitoring"."public"."provider" ("provider_id", "provider_name")
    (
        select "provider_id", "provider_name"
        from "provider__dbt_tmp214802852614"
    )
  