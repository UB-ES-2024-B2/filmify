import os
import pytest
from dotenv import load_dotenv
from supabase import create_client, Client

@pytest.fixture(scope='module')
def db_connection():
    # Load .env file from the parent directory
    load_dotenv(os.path.join(os.path.dirname(__file__), '../../../.env'))

    # Now you can access your environment variables
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    return supabase 

# Delete posts de Usuario Test en un Foro
def test_posts_delete(db_connection):
    response = db_connection.rpc("delete_posts_from_user", {'input_movie_id': 77, 'input_user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert response.data

# Posts de Foro Vacío
def test_posts_get1(db_connection):
    response = db_connection.rpc("get_posts", {'input_movie_id': 77}).execute()
    assert len(response.data) == 0

# Create Post
def test_post_create1(db_connection):
    response = db_connection.rpc("create_post", {'title': 'Título de Pueba', 'content': 'Contenido de prueba', 'input_movie_id': 77, 'user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert response.data

# Create Post de Película que no exite
def test_post_create2(db_connection):
    response = db_connection.rpc("create_post", {'title': 'Título de Pueba', 'content': 'Contenido de prueba', 'input_movie_id': 1, 'user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert response.data == False

# Create Post con Usuario equivocado
def test_post_create3(db_connection):
    response = db_connection.rpc("create_post", {'title': 'Título de Pueba', 'content': 'Contenido de prueba', 'input_movie_id': 1, 'user_id': '8a30b414-3548-0000-98de-1f849a77ef81'}).execute()
    assert response.data == False

# Create Post 2
def test_post_create4(db_connection):
    response = db_connection.rpc("create_post", {'title': 'Título de Pueba 2', 'content': 'Contenido de prueba 2', 'input_movie_id': 77, 'user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert response.data


# Posts de Foro 
def test_posts_get2(db_connection):
    response = db_connection.rpc("get_posts", {'input_movie_id': 77}).execute()
    assert len(response.data) == 2
    assert response.data[0]['title'] == 'Título de Pueba'
    assert response.data[0]['content'] == 'Contenido de prueba'
    assert response.data[0]['username'] == 'testuser'
    assert response.data[1]['title'] == 'Título de Pueba 2'
    assert response.data[1]['content'] == 'Contenido de prueba 2'
    assert response.data[1]['username'] == 'testuser'
