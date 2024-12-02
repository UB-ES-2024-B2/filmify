-- Function to calculate mean rating for a given user ID
create or replace function calculate_mean_rating(user_id uuid)
returns numeric
language plpgsql
as $$
declare
    mean_rating numeric;
begin
    -- Calculate the mean rating
    select coalesce(avg(rating), 0) 
    into mean_rating
    from "Valoraciones"
    where user_fk = user_id;

    -- Return the mean rating
    return mean_rating;
end;
$$;
