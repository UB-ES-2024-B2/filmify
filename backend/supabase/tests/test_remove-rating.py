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

user_id = 'c7228a59-c9ae-4eae-9dd0-47f61e87ecb6'
movie_id = 671

@pytest.fixture(scope='module', autouse=True)
def add_defaultrating(db_connection):
    db_connection.rpc('ratemovie', {'user_id': user_id, 'movie_id': movie_id, 'new_rating': 5}).execute()
    
# Quitar una valoración de una película
def test_removeExistentRating(db_connection):
    response = db_connection.rpc('removemovierating', {'user_id': user_id, 'movie_id': movie_id}).execute()
    assert response.data == [{'success': True, 'message': 'Rating removed successfully.'}]

# Quitar una valoración de una película que no has valorado ya
def test_removeNonExistentRating(db_connection):
    response = db_connection.rpc('removemovierating', {'user_id': user_id, 'movie_id': movie_id}).execute()
    assert response.data == [{'success': False, 'message': 'This user has not rated this movie.'}]

def test_incorrectUserID(db_connection):
    response = db_connection.rpc('removemovierating', {'user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022d', 'movie_id': movie_id}).execute()
    assert response.data == [{'success': False, 'message': 'User does not exist.'}]

def test_incorrectMovieID(db_connection):
    response = db_connection.rpc('removemovierating', {'user_id': user_id, 'movie_id': 1}).execute()
    assert response.data == [{'success': False, 'message': 'Movie does not exist.'}]
