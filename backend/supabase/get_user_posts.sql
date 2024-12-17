DROP FUNCTION get_user_posts(uuid);
create or replace function get_user_posts(input_user_id uuid)
returns table (post_id int, 
              username text, 
              title text, 
              content text, 
              image text, 
              creation_date timestamp, 
              votes int,
              movie_title text) as $$
begin
  return query 
  select p.id as post_id,
         u.user_name as username,
         p.title as title, 
         p.content as content, 
         p.image as image, 
         p.creation_date as creation_date,
        (p.upvotes - p.downvotes) as votes,
         m.title as movie_title
  from "Posts" p 
  join "Usuarios Auth" u on u.id = p.author_id 
  join "Foros" f on f.id = p.forum_id
  join "Peliculas" m on m.id = f.movie_id
  where p.author_id = input_user_id;
end;
$$ language plpgsql;
