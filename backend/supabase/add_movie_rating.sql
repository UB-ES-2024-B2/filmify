create or replace function ratemovie(user_id uuid, movie_id bigint, new_rating int)
returns table(success boolean, message text) as $$
begin
  if new_rating < 1 OR new_rating > 5 THEN
      return query values (false, 'Rating must be between 1 and 5.');
  elsif not  exists (select 1 from "Peliculas" where "Peliculas".id = movie_id) THEN 
    return query values (false, 'Movie does not exist.');
  elsif not exists ( select 1 from public."Usuarios Auth" where public."Usuarios Auth".id = user_id) THEN 
    return query values (false, 'User does not exist.');
  elsif exists ( select 1 from "Valoraciones" where user_fk = user_id and movie_fk = movie_id) THEN 
    UPDATE "Valoraciones" 
    SET rating = new_rating
    WHERE user_fk = user_id AND movie_fk = movie_id;
    return query values (true, 'Rating updated successfully.');
  else
    INSERT INTO "Valoraciones" (user_fk, movie_fk, rating)
    values (user_id, movie_id, new_rating);
    return query values (true, 'Rating added successfully.');
  end if;
end
$$ language plpgsql;