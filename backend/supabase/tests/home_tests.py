from supabase import create_client, Client

SUPABASE_URL = "https://ydzntmbvtktgeknydngv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlkem50bWJ2dGt0Z2Vrbnlkbmd2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkwMTczODcsImV4cCI6MjA0NDU5MzM4N30.eM6tB5yhGYJrVAngp5XPRWmZmpWdAmlAfZ7XlCQV1N4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Contador de aserciones pasadas y fallidas
asserts_passed = 0
asserts_failed = 0
total_asserts = 6  # Cambia este número si agregas más pruebas

# No hay peliculas en la base de datos
try:
    response = supabase.rpc("get_newest_movies_test", {'length': 5}).execute()
    assert len(response.data) == 0
    asserts_passed +=1
except AssertionError:
    asserts_failed +=1

try:
    response = supabase.rpc("get_popular_movies_test", {'length': 5}).execute()
    assert len(response.data) == 0
    asserts_passed +=1
except AssertionError:
    asserts_failed +=1

#Cargamos la base de datos
supabase.rpc('delete_peliculas_test').execute()

supabase.table('Peliculas_test').insert([
    {"title": "Buscando a Nemo", "release_date": "2003-05-30", "vote_count": 19117},
    {"title": "Piratas del Caribe: La maldición de la Perla Negra", "release_date": "2003-07-09", "vote_count": 20459},
    {"title": "Kill Bill: Volumen 1", "release_date": "2003-10-10", "vote_count": 17257},
    {"title": "Jarhead, el infierno espera", "release_date": "2005-11-04", "vote_count": 2845},
    {"title": "Los Simpson: La película", "release_date": "2007-07-25", "vote_count": 7909},
    ]).execute()

#Ejecución normal con películas en la base de datos
try:
    response = supabase.rpc("get_newest_movies_test", {'length': 5}).execute()
    assert len(response.data) == 5
    assert response.data[0]['title'] == "Los Simpson: La película"
    assert response.data[1]['title'] == "Jarhead, el infierno espera"
    assert response.data[2]['title'] == "Kill Bill: Volumen 1"
    assert response.data[3]['title'] == "Piratas del Caribe: La maldición de la Perla Negra"
    assert response.data[4]['title'] == "Buscando a Nemo"
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1

try:
    response = supabase.rpc("get_popular_movies_test", {'length': 5}).execute()
    assert len(response.data) == 5
    assert response.data[0]['title'] == "Piratas del Caribe: La maldición de la Perla Negra"
    assert response.data[1]['title'] == "Buscando a Nemo"
    assert response.data[2]['title'] == "Kill Bill: Volumen 1"
    assert response.data[3]['title'] == "Los Simpson: La película"
    assert response.data[4]['title'] == "Jarhead, el infierno espera"
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1

#Hay menos películas en la base de datos de las que se piden
try:
    response = supabase.rpc("get_newest_movies_test", {'length': 10}).execute()
    assert len(response.data) == 5
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1

try:
    response = supabase.rpc("get_popular_movies_test", {'length': 10}).execute()
    assert len(response.data) == 5
    asserts_passed +=1
except AssertionError:
    asserts_failed +=1


# Resultados finales
print(f"Total de aserciones: {total_asserts}, Aserciones pasadas: {asserts_passed}, Aserciones fallidas: {asserts_failed}")

supabase.rpc('delete_peliculas_test').execute()