create or replace function handle_rating_after_creation()
returns trigger
language plpgsql
as $$
begin
  update "Peliculas"
  set 
    vote_average = (vote_average*vote_count + new.rating)/(vote_count+1),
    vote_count = vote_count + 1
  where id = new.movie_fk;
  return new;
end;
$$;