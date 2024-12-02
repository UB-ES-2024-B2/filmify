create or replace function update_vote_post(input_user_id uuid, input_post_id bigint, vote boolean)
returns boolean as $$
begin
  if not  exists (select 1 from "Posts" where "Posts".id = input_post_id) THEN 
    return false;
  elsif not exists (select 1 from "Usuarios Auth" where id = input_user_id) THEN 
    return false;
  elsif not exists (select 1 from "Votos Post" where "Votos Post".user_id = input_user_id and "Votos Post".post_id = input_post_id) THEN 
    return false;
  else
    if not (select vote_type from "Votos Post" where "Votos Post".user_id = input_user_id and "Votos Post".post_id = input_post_id) = vote THEN 
      if vote THEN
        update "Posts"
        set upvotes = upvotes + 1, downvotes = downvotes - 1
        where "Posts".id = input_post_id;
      else
        update "Posts"
        set downvotes = downvotes + 1, upvotes = upvotes - 1
        where "Posts".id = input_post_id;
      end if;

      update "Votos Post"
      set vote_type = vote
      where "Votos Post".user_id = input_user_id and "Votos Post".post_id = input_post_id;
    end if;
    
    return true;
  end if;
end;
$$ language plpgsql;