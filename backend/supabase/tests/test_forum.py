import pytest
import os
from dotenv import load_dotenv
from supabase import create_client, Client

@pytest.fixture(scope='module')
def db_connection():
    # Load .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), '../../../.env'))

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase

def test_exists_forum_invalid_movie(db_connection):
    response = db_connection.rpc('exists_forum', {'input_movie_id': 9999}).execute()  # Non-existent movie ID
    assert response.data == False

def test_exists_forum_no_forum(db_connection):
    response = db_connection.rpc('exists_forum', {'input_movie_id': 22}).execute()  # Movie exists, but no forum
    assert response.data == False

def test_exists_forum_with_forum(db_connection):
    response = db_connection.rpc('exists_forum', {'input_movie_id': 12}).execute()  # Movie exists, and forum exists
    assert response.data == True

def test_create_forum_invalid_movie(db_connection):
    response = db_connection.rpc('create_forum', {
        'movie_id': 9999,  # Non-existent movie ID
        'name': 'Test Forum',
        'description': 'A forum for testing purposes'
    }).execute()
    assert response.data == False

def test_create_forum_valid_movie(db_connection):
    response = db_connection.rpc('create_forum', {
        'movie_id': 22,  # Valid movie ID
        'name': 'Test Forum',
        'description': 'A forum for testing purposes'
    }).execute()
    assert response.data == True

    try:
        # Verify forum was created
        forum = db_connection.table('Foros').select('*').eq('movie_id', 22).single().execute()
        assert forum.data['name'] == 'Test Forum'
        assert forum.data['description'] == 'A forum for testing purposes'
    finally:
        db_connection.table('Foros').delete().eq('movie_id', 22).execute()


def test_get_forum_info_invalid_movie(db_connection):
    response = db_connection.rpc('get_forum_info', {'input_movie_id': 9999}).execute()  # Non-existent movie ID
    assert response.data == []

def test_get_forum_info_no_forum(db_connection):
    response = db_connection.rpc('get_forum_info', {'input_movie_id': 22}).execute()  # Movie exists, but no forum
    assert response.data == []

def test_get_forum_info_with_forum(db_connection):
    response = db_connection.rpc('get_forum_info', {'input_movie_id': 12}).execute()  # Movie and forum exist
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Buscando a Nemo Foro'
    assert response.data[0]['description'] == 'Publicar post para la comunidad de esta película.'
