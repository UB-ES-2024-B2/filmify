create or replace function removemovierating(user_id uuid, movie_id bigint)
returns table(success boolean, message text) as $$
begin
  if not  exists (select 1 from "Peliculas" where "Peliculas".id = movie_id) THEN 
    return query values (false, 'Movie does not exist.');
  elsif not exists ( select 1 from public."Usuarios Auth" where public."Usuarios Auth".id = user_id) THEN 
    return query values (false, 'User does not exist.');
  elsif not exists ( select 1 from "Valoraciones" where user_fk = user_id and movie_fk = movie_id) THEN 
    return query values (false, 'This user has not rated this movie before.');
  else
    DELETE FROM "Valoraciones"
    WHERE user_fk = user_id and movie_fk = movie_id;
  end if;
end
$$ language plpgsql;