CREATE OR REPLACE FUNCTION public.get_movie_language(movie_id bigint) 
RETURNS TABLE (
  language_id int,
  language_name text
) 
LANGUAGE sql
AS $$
  SELECT "Idioma".id AS language_id,
         "Idioma".language AS language_name
  FROM public."Peliculas"
  JOIN public."Idioma"
    ON "Peliculas".language_fk = "Idioma".id
  WHERE "Peliculas".id = movie_id;
$$;
