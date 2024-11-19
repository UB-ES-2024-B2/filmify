create index if not exists idx_title_trgm on "Peliculas" using GIN (title gin_trgm_ops);

create
or replace function advanced_search (query text) returns setof "Peliculas" as $$
begin
  return query with combined_results as (
    select *, 1 as order_, 2.0 as similarity
    from "Peliculas"
    where to_tsvector(title)
      @@ to_tsquery(regexp_replace(query, ' ', '+', 'g'))
      
  union

    select *, 2 as order_, 2.0 as similarity
    from "Peliculas"
    where to_tsvector(title)
      @@ to_tsquery('simple', (regexp_replace(normalize_text(query), ' ', '+', 'g') || ':*'))
      
  union
    select *, 3 as order_, similarity(title, query) as similarity
    from "Peliculas"
    where similarity(title, query) >= 0.3),

  ranked_results as (
      select * ,
        row_number() over (partition by id order by order_, similarity desc) as rn
      from combined_results
    )

  select * from(
    select id, title, genre, release_date, year, poster_url, overview, "cast", vote_average, vote_count, director_fk, language_fk
    from ranked_results
    where rn = 1
    order by order_, similarity desc
  ) as final_result
  
  ; 
end;
$$ language plpgsql;
