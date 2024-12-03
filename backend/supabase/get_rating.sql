create or replace function get_rating(user_id uuid, movie_id bigint)
returns integer as $$
declare
  puntuacion integer;
begin
  -- Comprova si la pel·lícula existeix
  if not exists (select 1 from "Peliculas" where id = movie_id) then
    return null; -- Retorna NULL si la pel·lícula no existeix

  -- Comprova si l'usuari existeix
  elsif not exists (select 1 from "Usuarios Auth" where id = user_id) then
    return null; -- Retorna NULL si l'usuari no existeix

  -- Comprova si l'usuari ha valorat la pel·lícula
  elsif exists (select 1 from "Valoraciones" where user_fk = user_id and movie_fk = movie_id) then
    select rating into puntuacion
    from "Valoraciones"
    where user_fk = user_id and movie_fk = movie_id;

    return puntuacion; -- Retorna el valor de la puntuació
  else
    return null; -- Retorna NULL si no hi ha valoració
  end if;
end
$$ language plpgsql;
