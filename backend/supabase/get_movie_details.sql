create or replace function public.get_movie_details(movie_id bigint) 
returns table (
  id bigint,
  title text,
  release_date date,
  overview text,
  vote_average float,
  poster_url text
) 
language plpgsql 
as $$
begin
  return query
    select public."Peliculas".id, 
           public."Peliculas".title, 
           public."Peliculas".release_date, 
           public."Peliculas".overview, 
           public."Peliculas".vote_average, 
           public."Peliculas".poster_url
    from public."Peliculas"
    where public."Peliculas".id = movie_id;
end;
$$;
