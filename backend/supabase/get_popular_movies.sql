create or replace function get_popular_movies(length bigint) returns setof "Peliculas" as $$
  select * from "Peliculas"
  order by vote_count desc
  limit length;
$$ language sql
