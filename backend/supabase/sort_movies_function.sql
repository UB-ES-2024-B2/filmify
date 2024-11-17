create or replace function sort_movies(genre_ text, type text, length bigint)
returns setof "Peliculas" as $$
begin
  if type = 'alfabético' then 
    return query 
    select * from filter_movies(genre_, length)
    order by title asc;
  elsif type = 'fecha' then
    return query 
    select * from filter_movies(genre_, length)
    order by release_date desc;
  else 
    return query 
    select * from filter_movies(genre_, length);
  end if;
end
$$ language plpgsql;