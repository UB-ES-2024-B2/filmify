create or replace function exists_forum(input_movie_id bigint)
returns boolean as $$
begin
  if not  exists (select 1 from "Peliculas" where id = input_movie_id) THEN 
    return false;
  elsif not exists (select 1 from "Foros" where movie_id = input_movie_id) THEN 
    return false;
  else
    return true;
  end if;
end;
$$ language plpgsql;