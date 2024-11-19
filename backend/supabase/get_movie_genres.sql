create or replace function public.get_movie_genres(movie_id bigint) 
returns table (
  genre_id int,
  genre_name text
) 
language sql
as $$
  select genres_peliculas.genre_fk,
         "Genres".name
  from public.genres_peliculas
  join public."Genres"
    on genres_peliculas.genre_fk = "Genres".id
  where genres_peliculas.movie_fk = movie_id;
$$;
