
      
        
            delete from "earth_monitoring"."public"."owner"
            where (
                owner_id) in (
                select (owner_id)
                from "owner__dbt_tmp214802501580"
            );

        
    

    insert into "earth_monitoring"."public"."owner" ("owner_id", "owner_name")
    (
        select "owner_id", "owner_name"
        from "owner__dbt_tmp214802501580"
    )
  