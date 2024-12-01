create or replace function create_forum(movie_id bigint, name text default null, description text default null)
returns boolean as $$
begin
  if not  exists (select 1 from "Peliculas" where "Peliculas".id = movie_id) THEN 
    return false;
  else
    insert into "Foros" (name, description, movie_id)
    values (name, description, movie_id);
    return true;
  end if;
end;
$$ language plpgsql;