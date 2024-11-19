create or replace function public.get_movie_cast(movie_id bigint) 
returns table (
  actor_id int,
  actor_name text
) 
language sql
as $$
  select actores_peliculas.actor_fk,
         "Actores".name
  from public.actores_peliculas
  join public."Actores"
    on actores_peliculas.actor_fk = "Actores".id
  where actores_peliculas.movie_fk = movie_id;
$$;
