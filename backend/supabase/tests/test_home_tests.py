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
@pytest.fixture
def setup_database(db_connection):
    db_connection.rpc('delete_peliculas_test').execute()

    db_connection.table('Peliculas_test').insert([
        {"title": "Buscando a Nemo", "release_date": "2003-05-30", "vote_count": 19117},
        {"title": "Piratas del Caribe: La maldición de la Perla Negra", "release_date": "2003-07-09",
         "vote_count": 20459},
        {"title": "Kill Bill: Volumen 1", "release_date": "2003-10-10", "vote_count": 17257},
        {"title": "Jarhead, el infierno espera", "release_date": "2005-11-04", "vote_count": 2845},
        {"title": "Los Simpson: La película", "release_date": "2007-07-25", "vote_count": 7909},
    ]).execute()
def test_empty_database_newest_movies(db_connection):
    response = db_connection.rpc("get_newest_movies_test", {'length': 5}).execute()
    assert len(response.data) == 0

def test_empty_database_popular_movies(db_connection):
    response = db_connection.rpc("get_popular_movies_test", {'length': 5}).execute()
    assert len(response.data) == 0

def test_get_newest_movies(db_connection, setup_database):
    response = db_connection.rpc("get_newest_movies_test", {'length': 5}).execute()
    assert len(response.data) == 5
    assert response.data[0]['title'] == "Los Simpson: La película"
    assert response.data[1]['title'] == "Jarhead, el infierno espera"
    assert response.data[2]['title'] == "Kill Bill: Volumen 1"
    assert response.data[3]['title'] == "Piratas del Caribe: La maldición de la Perla Negra"
    assert response.data[4]['title'] == "Buscando a Nemo"

def test_get_popular_movies(db_connection, setup_database):
    response = db_connection.rpc("get_popular_movies_test", {'length': 5}).execute()
    assert len(response.data) == 5
    assert response.data[0]['title'] == "Piratas del Caribe: La maldición de la Perla Negra"
    assert response.data[1]['title'] == "Buscando a Nemo"
    assert response.data[2]['title'] == "Kill Bill: Volumen 1"
    assert response.data[3]['title'] == "Los Simpson: La película"
    assert response.data[4]['title'] == "Jarhead, el infierno espera"

def test_get_newest_movies_less_than_expected(db_connection, setup_database):
    response = db_connection.rpc("get_newest_movies_test", {'length': 10}).execute()
    assert len(response.data) == 5

def test_get_popular_movies_less_than_expected(db_connection, setup_database):
    response = db_connection.rpc("get_popular_movies_test", {'length': 10}).execute()
    assert len(response.data) == 5
