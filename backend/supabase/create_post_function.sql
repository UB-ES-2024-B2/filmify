create or replace function create_post(title text, content text, input_movie_id bigint, user_id uuid, image text default null)
returns boolean as $$
begin
  if not  exists (select 1 from "Peliculas" where "Peliculas".id = input_movie_id) THEN 
    return false;
  elsif not exists ( select 1 from "Usuarios Auth" where id = user_id) THEN 
    return false;
  else
    insert into "Posts" (title, content, image, forum_id, author_id)
    values (title, content, image, (select id from "Foros" where "Foros".movie_id = input_movie_id), user_id);
    return true;
  end if;
end;
$$ language plpgsql;
