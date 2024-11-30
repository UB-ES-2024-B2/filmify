create or replace function ratemovie(user_id uuid, movie_id bigint, rating int)
returns table(success boolean, message text) as $$
begin
    IF rating < 1 OR rating > 5 THEN
        RETURN query value (false, 'Rating value is incorrect';)
    END IF;
  if not  exists (select 1 from "Peliculas" where "Peliculas".id = movie_id) THEN 
    return query values (false, 'Movie does not exist');
  elsif not exists ( select 1 from auth.users where auth.users.id = user_id) THEN 
    return query values (false, 'User does not exist');
  elsif exists ( select 1 from "Valoraciones" where user_fk = user_id and movie_fk = movie_id) THEN 
    UPDATE "Valoraciones" v
    SET v.rating = rating
    WHERE v.user_fk = user_id AND v.movie_fk = movie_id;
    return query values (true, 'Rating updated successfully');
  else
    INSERT INTO "Valoraciones" (user_fk, movie_fk, rating)
    values (user_id, movie_id, rating);
    return query values (true, 'Rating addedd successfully');
  end if;
end
$$ language plpgsql;