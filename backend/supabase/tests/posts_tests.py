import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env file from the parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '../../../.env'))

# Now you can access your environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Contador de aserciones pasadas y fallidas
asserts_passed = 0
asserts_failed = 0
total_asserts = 7  # Cambia este número si agregas más pruebas

# Pruebas

# - Delete posts de Usuario Test en un Foro
try:
    responseDelete = supabase.rpc("delete_posts_from_user", {'input_movie_id': 77, 'input_user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert responseDelete.data
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en eliminación de posts")

# - Posts de Foro Vacío
try:
    responseGet1 = supabase.rpc("get_posts", {'input_movie_id': 77}).execute()
    assert len(responseGet1.data) == 0
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en obtener posts (vacío)")

# - Create Post
try:
    responseCreate1 = supabase.rpc("create_post", {'title': 'Título de Pueba', 'content': 'Contenido de prueba', 'input_movie_id': 77, 'user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert responseCreate1.data
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en crear post 1")

# - Create Post de Película que no existe
try:
    responseCreate2 = supabase.rpc("create_post", {'title': 'Título de Pueba', 'content': 'Contenido de prueba', 'input_movie_id': 1, 'user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert responseCreate2.data == False
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en crear post con película inexistente")

# - Create Post con Usuario equivocado
try:
    responseCreate3 = supabase.rpc("create_post", {'title': 'Título de Pueba', 'content': 'Contenido de prueba', 'input_movie_id': 1, 'user_id': '8a30b414-3548-0000-98de-1f849a77ef81'}).execute()
    assert responseCreate3.data == False
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en crear post con usuario incorrecto")

# - Create Post 2
try:
    responseCreate4 = supabase.rpc("create_post", {'title': 'Título de Pueba 2', 'content': 'Contenido de prueba 2', 'input_movie_id': 77, 'user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert responseCreate4.data
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en crear post 2")

# - Posts de Foro
try:
    responseGet2 = supabase.rpc("get_posts", {'input_movie_id': 77}).execute()
    assert len(responseGet2.data) == 2
    assert responseGet2.data[0]['title'] == 'Título de Pueba'
    assert responseGet2.data[0]['content'] == 'Contenido de prueba'
    assert responseGet2.data[0]['username'] == 'testuser'
    assert responseGet2.data[1]['title'] == 'Título de Pueba 2'
    assert responseGet2.data[1]['content'] == 'Contenido de prueba 2'
    assert responseGet2.data[1]['username'] == 'testuser'
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en obtener posts (con datos)")
