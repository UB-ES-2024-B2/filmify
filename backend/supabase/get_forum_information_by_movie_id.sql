create or replace function get_forum_info(input_movie_id bigint)
returns table (name text, description text) as $$
begin
  if not  exists (select 1 from "Peliculas" where id = input_movie_id) THEN 
    return ;
  elsif not exists (select 1 from "Foros" where movie_id = input_movie_id) THEN 
    return ;
  else
    return query select "Foros".name, "Foros".description from "Foros" where movie_id = input_movie_id;
  end if;
end;
$$ language plpgsql;