create or replace function delete_post_by_id(input_post_id bigint, input_user_id uuid)
returns boolean as $$
begin
  if not  exists (select 1 from "Posts" where "Posts".id = input_post_id) THEN 
    return false;
  elsif not exists ( select 1 from "Usuarios Auth" where id = input_user_id) THEN 
    return false;
  else
    delete from "Posts"
    where "Posts".id = input_post_id and "Posts".author_id = input_user_id;
    return true;
  end if;
end;
$$ language plpgsql;