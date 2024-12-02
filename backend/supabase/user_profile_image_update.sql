create or replace function add_profile_pic(input_user_id uuid, image text)
returns boolean as $$
begin
  if not exists (select 1 from "Usuarios Auth" where id = input_user_id) THEN 
    return false;
  else
    update "Usuarios Auth"
    set profile_image_url = image
    where id = input_user_id;
    return true;
  end if;
end;
$$ language plpgsql;