
      
        
            delete from "earth_monitoring"."public"."country"
            where (
                country_id) in (
                select (country_id)
                from "country__dbt_tmp214802511559"
            );

        
    

    insert into "earth_monitoring"."public"."country" ("country_id", "country_code", "country_name")
    (
        select "country_id", "country_code", "country_name"
        from "country__dbt_tmp214802511559"
    )
  