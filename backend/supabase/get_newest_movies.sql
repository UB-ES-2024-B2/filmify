create or replace function get_newest_movies(length bigint) returns setof "Peliculas" as $$
  select * from "Peliculas"
  where release_date is not null
  order by release_date::DATE desc
  limit length;
$$ language sql