
      
        
            delete from "earth_monitoring"."public"."parameter"
            where (
                parameter_id) in (
                select (parameter_id)
                from "parameter__dbt_tmp214802473612"
            );

        
    

    insert into "earth_monitoring"."public"."parameter" ("parameter_id", "name", "units", "display_name")
    (
        select "parameter_id", "name", "units", "display_name"
        from "parameter__dbt_tmp214802473612"
    )
  