create or replace function remove_from_wishlist(user_id uuid, movie_id bigint)
returns boolean as $$
begin
  -- Verifica que la pel·lícula existeix
  if not exists (select 1 from "Peliculas" where "Peliculas".id = movie_id) then
    return false;

  -- Verifica que l'usuari existeix
  elsif not exists (select 1 from "Usuarios Auth" where id = user_id) then
    return false;

  -- Verifica que la pel·lícula està als favorits
  elsif not exists (select 1 from "Wishlist" where user_fk = user_id and movie_fk = movie_id) then
    return false;

  -- Elimina la pel·lícula de la llista de favorits
  else
    delete from "Wishlist"
    where user_fk = user_id and movie_fk = movie_id;
    return true;
  end if;
end
$$ language plpgsql;
