create or replace function check_auth_email_exists(email_input text)
returns boolean as $$
declare
    email_found boolean;
begin
    select exists (
        select 1
        from auth.users
        where email = email_input
    ) into email_found;

    return email_found;
end;
$$ language plpgsql security definer;
