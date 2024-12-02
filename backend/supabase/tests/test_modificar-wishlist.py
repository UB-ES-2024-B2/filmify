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

userID = '0c518d94-a5bb-4a29-9d9c-1fb022a5a404'
movieID = 12

@pytest.fixture(scope='module')
def vaciar_lista(db_connection):
    # Vaciar la lista de favoritos de este usuario primero para los tests
    db_connection.table('Wishlist').delete().eq('user_fk', userID).execute()

#################
# Add tests
#################

def test_addToListWrongMovie(db_connection):
    response = db_connection.rpc('add_to_wishlist', {'user_id': userID, 'movie_id': 1}).execute()
    assert response.data == False

def test_addToListWrongUser(db_connection):
    response = db_connection.rpc('add_to_wishlist', {'user_id': '0c518e96-a5bb-4a29-9d9c-1fb022a5a404', 'movie_id': movieID}).execute()
    assert response.data == False

def test_addToList(db_connection):
    response = db_connection.rpc('add_to_wishlist', {'user_id': userID, 'movie_id': movieID}).execute()
    assert response.data == True

def test_addToListAgain(db_connection):
    response = db_connection.rpc('add_to_wishlist', {'user_id': userID, 'movie_id': movieID}).execute()
    assert response.data == False

#################
# Check if already exists tests
#################

def test_checkIfAlreadyExistsWrongMovie(db_connection):
    response = db_connection.rpc('is_wished', {'user_id': userID, 'movie_id': 1}).execute()
    assert response.data == False

def test_checkIfAlreadyExistsWrongUser(db_connection):
    response = db_connection.rpc('is_wished', {'user_id': '0c518e96-a5bb-4a29-9d9c-1fb022a5a404', 'movie_id': movieID}).execute()
    assert response.data == False

def test_checkIfAlreadyExists(db_connection):
    response = db_connection.rpc('is_wished', {'user_id': userID, 'movie_id': movieID}).execute()
    assert response.data == True

#################
# Remove tests
#################

def test_removeFromListWrongMovie(db_connection):
    response = db_connection.rpc('remove_from_wishlist', {'user_id': userID, 'movie_id': 1}).execute()
    assert response.data == False

def test_removeFromListWrongUser(db_connection):
    response = db_connection.rpc('remove_from_wishlist', {'user_id': '0c518e96-a5bb-4a29-9d9c-1fb022a5a404', 'movie_id': movieID}).execute()
    assert response.data == False

def test_removeFromList(db_connection):
    response = db_connection.rpc('remove_from_wishlist', {'user_id': userID, 'movie_id': movieID}).execute()
    assert response.data == True

def test_removeFromListAgain(db_connection):
    response = db_connection.rpc('remove_from_wishlist', {'user_id': userID, 'movie_id': movieID}).execute()
    assert response.data == False

