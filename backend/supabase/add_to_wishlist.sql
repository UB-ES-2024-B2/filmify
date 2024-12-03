create or replace function add_to_wishlist(user_id uuid, movie_id bigint)
returns boolean as $$
begin
  if not  exists (select 1 from "Peliculas" where "Peliculas".id = movie_id) THEN 
    return false;
  elsif not exists ( select 1 from "Usuarios Auth" where id = user_id) THEN 
    return false;
  elsif exists ( select 1 from "Wishlist" where user_fk = user_id and movie_fk = movie_id) THEN 
    return false;
  else
    insert into "Wishlist" (user_fk, movie_fk, created_at)
    values (user_id, movie_id, current_timestamp);
    return true;
  end if;
end
$$ language plpgsql;