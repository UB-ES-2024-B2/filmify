create or replace function login(username text, input_password text)
returns table (signInSuccessful boolean, errorMessage text) as $$
begin
  if username is null or trim(username) = '' THEN 
  return query select false,'Error: El campo username no puede estar vacío.';
  elsif input_password is null or trim(input_password) = '' THEN 
  return query select false,'Error: El campo password no puede estar vacío.';
  elsif not exists ( select 1 from "Usuarios" where user_name = trim(username)) THEN 
  return query select false,'Error: El nombre de usuario no existe.';
  elsif check_password(input_password, (select password from "Usuarios" where user_name = trim(username))) THEN
  return query select true,'Inicio de sesión correcto.';
  else
  return query select false,'Error: La contraseña no coincide.';
  end if;
end;
$$ language plpgsql;