create or replace function get_favorites(user_id uuid)
returns setof "Peliculas" as $$
begin
  if not exists ( select 1 from auth.users where auth.users.id = user_id) THEN 
    return;
  else
    return query ( 
      select id, title, genre, release_date, year, poster_url, overview, "cast", vote_average, vote_count, director_fk, language_fk
      from "Peliculas"
      inner join "Favorites list" on "Favorites list".movie_fk = "Peliculas".id
      where "Favorites list".user_fk = user_id
    );
  end if;
end
$$ language plpgsql;