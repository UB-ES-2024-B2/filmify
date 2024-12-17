create or replace function handle_rating_after_delete()
returns trigger
language plpgsql
as $$
begin
  update "Peliculas"
  set 
    vote_average = (vote_average * vote_count - OLD.rating) / (vote_count - 1),
    vote_count = vote_count - 1
  where id = OLD.movie_fk;

  return OLD;
end;
$$;
