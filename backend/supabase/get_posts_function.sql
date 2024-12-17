create or replace function get_posts(input_movie_id bigint, input_user_id uuid default null)
returns table (post_id int, 
              username text, 
              title text, 
              content text, 
              image text, 
              creation_date timestamp, 
              votes int, 
              hasVoted boolean, 
              vote boolean,
              owner boolean) as $$
begin
  if not  exists (select 1 from "Peliculas" where "Peliculas".id = input_movie_id) THEN 
    return;
  elsif not exists (select 1 from "Usuarios Auth" where id = input_user_id) THEN 
    return query (
      select p.id as post_id,
         u.user_name as username,
         p.title as title, 
         p.content as content, 
         p.image as image, 
         p.creation_date as creation_date,
        (p.upvotes - p.downvotes) as votes,
        false as hasVoted,
        false as vote,
        false as owner
      from "Posts" p 
      join "Usuarios Auth" u
      on u.id = p.author_id
      where p.forum_id = (select id from "Foros" where "Foros".movie_id = input_movie_id)
      order by votes desc, post_id asc
    );
  else
    return query (
      select p.id as post_id,
         u.user_name as username,
         p.title as title, 
         p.content as content, 
         p.image as image, 
         p.creation_date as creation_date,
        (p.upvotes - p.downvotes) as votes,
        exists (select 1 from "Votos Post" where "Votos Post".user_id = input_user_id and "Votos Post".post_id = p.id) as hasVoted,
        (select vote_type from "Votos Post" where "Votos Post".user_id = input_user_id and "Votos Post".post_id = p.id) as vote,
        (p.author_id = input_user_id) as owner
      from "Posts" p 
      join "Usuarios Auth" u
      on u.id = p.author_id
      where p.forum_id = (select id from "Foros" where "Foros".movie_id = input_movie_id)      
      order by votes desc, post_id asc
    );
  end if;
end;
$$ language plpgsql;
