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

def test_invalid_user(db_connection):
    response = db_connection.rpc('add_profile_pic', {'input_user_id': "f3cf42e6-6380-4ed7-95c0-05eceae1022d",
                                                     'image': "https://firebasestorage.googleapis.com/v0/b/filmify-c99db.firebasestorage.app/o/userImages%2Ff3cf42e6-6380-4ed7-95c0-05eceae1022c.png?alt=media"}).execute()
    assert response.data == False

def test_normal_execution(db_connection):
    response = db_connection.rpc('add_profile_pic', {'input_user_id': "f3cf42e6-6380-4ed7-95c0-05eceae1022c",
                                                     'image': "https://firebasestorage.googleapis.com/v0/b/filmify-c99db.firebasestorage.app/o/userImages%2Ff3cf42e6-6380-4ed7-95c0-05eceae1022c.png?alt=media"}).execute()
    assert response.data == True