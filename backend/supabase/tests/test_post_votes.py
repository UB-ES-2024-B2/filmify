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

def test_update_vote_post_invalid_post(db_connection):
    response = db_connection.rpc('update_vote_post', {
        'input_user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022c',
        'input_post_id': 9999,  # Non-existent post ID
        'vote': True
    }).execute()
    assert response.data == False

def test_update_vote_post_invalid_user(db_connection):
    response = db_connection.rpc('update_vote_post', {
        'input_user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022d',
        'input_post_id': 1,
        'vote': True
    }).execute()
    assert response.data == False

def test_update_vote_post_no_existing_vote(db_connection):
    response = db_connection.rpc('update_vote_post', {
        'input_user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022c',
        'input_post_id': 40,
        'vote': True
    }).execute()
    assert response.data == False

def test_vote_post_invalid_post(db_connection):
    response = db_connection.rpc('vote_post', {
        'input_user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022c',
        'input_post_id': 9999,  # Non-existent post ID
        'vote': True
    }).execute()
    assert response.data == False

def test_vote_post_invalid_user(db_connection):
    response = db_connection.rpc('vote_post', {
        'input_user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022d',
        'input_post_id': 1,
        'vote': True
    }).execute()
    assert response.data == False

def test_vote_post_existing_vote(db_connection):
    response = db_connection.rpc('vote_post', {
        'input_user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022c',
        'input_post_id': 1,
        'vote': True
    }).execute()
    assert response.data == False

