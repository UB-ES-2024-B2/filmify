CREATE OR REPLACE FUNCTION get_wishlist(user_id uuid)
RETURNS TABLE (
  id bigint,
  title text,
  poster_url text,
  vote_average float,
  vote_count int
)
LANGUAGE sql
AS $$
  SELECT p.id, p.title, p.poster_url, p.vote_average, p.vote_count
  FROM public."Peliculas" p
  INNER JOIN public."Wishlist" w ON w.movie_fk = p.id
  WHERE w.user_fk = user_id;
$$;
