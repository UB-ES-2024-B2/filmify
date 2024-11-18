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
        {"title": "Buscando a Nemo", "genre": "['Animación', 'Familia']", "release_date": "2003-05-30", "vote_count": 19117},
        {"title": "Piratas del Caribe: La maldición de la Perla Negra", "genre": "['Aventura', 'Fantasía', 'Acción']",
         "release_date": "2003-07-09", "vote_count": 20459},
        {"title": "Kill Bill: Volumen 1", "genre": "['Acción', 'Crimen']", "release_date": "2003-10-10", "vote_count": 17257},
        {"title": "Jarhead, el infierno espera", "genre": "['Drama', 'Bélica']", "release_date": "2005-11-04", "vote_count": 2845},
        {"title": "Los Simpson: La película", "genre": "['Animación', 'Comedia', 'Familia']", "release_date": "2007-07-25",
         "vote_count": 7909},
        {"title": "Piratas del Caribe: El cofre del hombre muerto", "genre": "['Aventura', 'Fantasía', 'Acción']",
         "release_date": "2006-07-06", "vote_count": 15794},
    ]).execute()
@pytest.fixture
def empty_test_data(db_connection):
    db_connection.rpc('delete_peliculas_test').execute()
def test_empty_database_filter(db_connection, empty_test_data):
    response = db_connection.rpc('filter_movies_test', {'genre_': "Animación", 'length': 10}).execute()
    assert len(response.data) == 0
def test_empty_database_sort(db_connection, empty_test_data):
    response = db_connection.rpc('sort_movies_test', {'genre_': "Animación", 'type': "alfabético", 'length': 10}).execute()
    assert len(response.data) == 0
def test_filter(db_connection, setup_test_data):
    response = db_connection.rpc('filter_movies_test', {'genre_': "Animación", 'length': 10}).execute()
    assert len(response.data) == 2
    for i in range(len(response.data)):
        assert "Animación" in response.data[i]['genre']

def test_alphabetic_sort(db_connection, setup_test_data):
    response = db_connection.rpc('sort_movies_test', {'genre_': "Acción", 'type': "alfabético", 'length': 10}).execute()
    assert len(response.data) == 3
    print(response.data)
    assert response.data[0]['title'] == "Kill Bill: Volumen 1"
    assert response.data[1]['title'] == "Piratas del Caribe: El cofre del hombre muerto"
    assert response.data[2]['title'] == "Piratas del Caribe: La maldición de la Perla Negra"

def test_date_sort(db_connection, setup_test_data):
    response = db_connection.rpc('sort_movies_test', {'genre_': "Acción", 'type': "fecha", 'length': 10}).execute()
    assert len(response.data) == 3
    assert response.data[0]['release_date'] == "2006-07-06"
    assert response.data[1]['release_date'] == "2003-10-10"
    assert response.data[2]['release_date'] == "2003-07-09"
