create or replace function handle_rating_after_update()
returns trigger
language plpgsql
as $$
declare
  old_rating numeric;
begin
  update "Peliculas"
  set 
    vote_average = (vote_average * vote_count - OLD.rating + NEW.rating) / vote_count
  where id = NEW.movie_fk;
  
  return NEW;
end;
$$;
