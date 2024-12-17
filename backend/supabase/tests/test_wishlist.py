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

# Como solo implementamos que se muestren las peliculas, hemos creado algunas relaciones ya en la base de datos.
# En el siguente sprint implementaremos la funcionalidad que queda.

# Usuario con Wishlist
def test_wish_list_two(db_connection):
    response = db_connection.rpc("get_wishlist", {'user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022c'}).execute()
    assert len(response.data) == 2
    assert response.data == [{'id': 12, 'title': 'Buscando a Nemo', 'poster_url': 'https://image.tmdb.org/t/p/original/jPhak722pNGxQIXSEfeWIUqBrO5.jpg', 'vote_average': 3.9095, 'vote_count': 19117}, {'id': 24, 'title': 'Kill Bill: Volumen 1', 'poster_url': 'https://image.tmdb.org/t/p/original/lfj709InbmljVqAXgUk2qjnujNN.jpg', 'vote_average': 3.9855, 'vote_count': 17257}]

# Usuario sin Wishlist
def test_wish_list_empty(db_connection):
    response = db_connection.rpc("get_wishlist", {'user_id': '1f874ad7-1203-4d6b-bade-73b76582b7e7'}).execute()
    assert len(response.data) == 0
    assert response.data == []
