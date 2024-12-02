create or replace function get_posts(input_movie_id bigint)
returns table (post_id int, username text, title text, content text, images text[], creation_date timestamp, votes int) as $$
begin
  if not  exists (select 1 from "Peliculas" where "Peliculas".id = input_movie_id) THEN 
    return;
  else
    return query (
      select p.id as post_id,
         u.user_name as username,
         p.title as title, 
         p.content as content, 
         p.images as images, 
         p.creation_date as creation_date,
        (p.upvotes - p.downvotes) as votes
      from "Posts" p 
      join "Usuarios Auth" u
      on u.id = p.author_id
      where p.forum_id = (select id from "Foros" where "Foros".movie_id = input_movie_id)
    );
  end if;
end;
$$ language plpgsql;