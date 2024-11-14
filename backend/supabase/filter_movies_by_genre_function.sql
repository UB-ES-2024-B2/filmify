create or replace function filter_movies(genre_ text, length bigint)
returns setof "Peliculas" as $$
begin
  return query 
    select * from "Peliculas"
    where genre like ('%' || genre_ || '%')
    order by vote_count desc
    limit length;
end
$$ language plpgsql;