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

# Pruebas
movie_id = 12

# - Movie Details
def test_movie_details(db_connection):
    response = db_connection.rpc("get_movie_details", {'movie_id': movie_id}).execute()
    assert len(response.data) == 1
    assert response.data[0] == {'id': 12, 'title': 'Buscando a Nemo', 'release_date': '2003-05-30', 'overview': 'Nemo, un pececillo, hijo único muy querido y protegido por su padre, ha sido capturado en un arrecife australiano y ahora vive en una pecera en la oficina de un dentista de Sidney. El tímido padre de Nemo se embarcará en una peligrosa aventura para rescatar a su hijo. Pero Nemo y sus nuevos amigos tienen también un astuto plan para escapar de la pecera y volver al mar.', 'vote_average': 7.819, 'poster_url': 'https://image.tmdb.org/t/p/original/jPhak722pNGxQIXSEfeWIUqBrO5.jpg'}

# - Movie Genres
def test_movie_genres(db_connection):
    response = db_connection.rpc("get_movie_genres", {'movie_id': movie_id}).execute()
    assert len(response.data) == 2
    assert response.data[0] == {'genre_id': 3, 'genre_name': 'Familia'}, {'genre_id': 14, 'genre_name': 'Animación'}

# - Movie Cast
def test_movie_cast(db_connection):
    response = db_connection.rpc("get_movie_cast", {'movie_id': movie_id}).execute()
    assert len(response.data) == 10
    assert response.data == [{'actor_id': 4203, 'actor_name': 'Willem Dafoe'}, {'actor_id': 4619, 'actor_name': 'Allison Janney'}, {'actor_id': 4904, 'actor_name': 'Stephen Root'}, {'actor_id': 6151, 'actor_name': 'Brad Garrett'}, {'actor_id': 7473, 'actor_name': 'Geoffrey Rush'}, {'actor_id': 8581, 'actor_name': 'Albert Brooks'}, {'actor_id': 10196, 'actor_name': 'Ellen DeGeneres'}, {'actor_id': 10197, 'actor_name': 'Alexander Gould'}, {'actor_id': 10198, 'actor_name': 'Austin Pendleton'}, {'actor_id': 10199, 'actor_name': 'Vicki Lewis'}]

# - Movie Director
def test_movie_director(db_connection):
    response = db_connection.rpc("get_movie_director", {'movie_id': movie_id}).execute()
    assert len(response.data) == 1
    assert response.data == [{'director_id': 716, 'director_name': 'Andrew Stanton'}]


# - Movie Language
def test_movie_language(db_connection):
    response = db_connection.rpc("get_movie_language", {'movie_id': movie_id}).execute()
    assert len(response.data) == 1
    assert response.data == [{'language_id': 1021, 'language_name': 'Inglés'}]
