create or replace function is_favorited(user_id uuid, movie_id bigint)
returns boolean as $$
begin
  if not exists (select 1 from "Peliculas" where "Peliculas".id = movie_id) then
    return false;

  elsif not exists (select 1 from "Usuarios Auth" where id = user_id) then
    return false;

  elsif exists (select 1 from "Favorites list" where user_fk = user_id and movie_fk = movie_id) then
    return true;

  else
    return false;
  end if;
end
$$ language plpgsql;
