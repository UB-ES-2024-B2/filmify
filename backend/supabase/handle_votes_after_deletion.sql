create or replace function handle_votes_after_deletion()
returns trigger
language plpgsql
as $$
begin
  if old.vote_type THEN 
    update "Posts"
    set upvotes = upvotes - 1
    where "Posts".id = old.post_id;
  else
    update "Posts"
    set downvotes = downvotes - 1
    where "Posts".id = old.post_id;
  end if;
  return old;
end;
$$;