create or replace function register_user (username text, password text, s_email text) 
returns table (signUpSuccessful boolean, errorMessage text) as $$
begin
  if username is null or trim(username) = '' THEN 
  return query select false,'Error: El campo username no puede estar vacío.';
  elsif password is null or trim(password) = '' THEN 
  return query select false,'Error: El campo password no puede estar vacío.';
  elsif s_email is null or trim(s_email) = '' THEN 
  return query select false,'Error: El campo email no puede estar vacío.';
  elsif exists ( select 1 from "Usuarios" where user_name = trim(username)) THEN 
  return query select false,'Error: El nombre de usuario ya está en uso.';
  elsif exists ( select 1 from "Usuarios" where email = trim(s_email)) THEN 
  return query select false,'Error: La dirección de correo ya está registrada.';
  else
  insert into "Usuarios" (user_name, email, password, is_admin, profile_image, bio, creation_date)
  values (username, s_email, hash_password(password), false, '', '', current_timestamp);
  return query select true,'Usuario creado exitosamente.';
  end if;
end;
$$ language plpgsql;