import pytest
import os
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

@pytest.fixture
def setup_test_data(db_connection):
    # Cargamos la base de datos
    db_connection.rpc('delete_peliculas_test').execute()

    db_connection.table('Peliculas_test').insert([
        {"title": "Buscando a Nemo", "release_date": "2003-05-30", "vote_count": 19117},
        {"title": "Piratas del Caribe: La maldición de la Perla Negra", "release_date": "2003-07-09",
         "vote_count": 20459},
        {"title": "Kill Bill: Volumen 1", "release_date": "2003-10-10", "vote_count": 17257},
        {"title": "Jarhead, el infierno espera", "release_date": "2005-11-04", "vote_count": 2845},
        {"title": "Los Simpson: La película", "release_date": "2007-07-25", "vote_count": 7909},
        {"title": "Piratas del Caribe: El cofre del hombre muerto", "release_date": "2006-07-06", "vote_count": 15794},

    ]).execute()
@pytest.fixture
def empty_test_data(db_connection):
    db_connection.rpc('delete_peliculas_test').execute()
def test_empty_advanced_search(db_connection, empty_test_data):
    response = db_connection.rpc('advanced_search_test', {'query': "Buscando"}).execute()
    assert len(response.data) == 0

def test_unique_advanced_search(db_connection, setup_test_data):
    response = db_connection.rpc('advanced_search_test', {'query': "Buscando"}).execute()
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Buscando a Nemo"

def test_multiple_advanced_search(db_connection, setup_test_data):
    response = db_connection.rpc('advanced_search_test', {'query': "Piratas"}).execute()
    assert len(response.data) == 2

def test_no_existing_advanced_search(db_connection, setup_test_data):
    response = db_connection.rpc('advanced_search_test', {'query': "Testing"}).execute()
    assert len(response.data) == 0