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

@pytest.fixture
def setup_test_data(db_connection):
    db_connection.table('Posts_test').insert([
        {"title": "test", "content": "test", "forum_id": 1, "author_id": userID, "creation_date": "2024-10-30"},
        {"title": "test", "content": "test", "forum_id": 1, "author_id": userID, "creation_date": "2024-12-01"},
        {"title": "test", "content": "test", "forum_id": 1, "author_id": userID, "creation_date": "2023-10-29"},
        {"title": "test", "content": "test", "forum_id": 1, "author_id": userID, "creation_date": "2024-05-01"},
        {"title": "test", "content": "test", "forum_id": 1, "author_id": userID, "creation_date": "2024-01-30"},
        {"title": "test", "content": "test", "forum_id": 1, "author_id": userID, "creation_date": "2023-03-29"},
    ]).execute()

@pytest.fixture
def setup_test_data_one_post(db_connection):
    db_connection.table('Posts_test').insert([
        {"title": "test", "content": "test", "forum_id": 1, "author_id": userID, "creation_date": "2024-12-01"},
    ]).execute()
def test_get_latest_posts(db_connection, setup_test_data):
    response = db_connection.rpc('get_latest_posts_test', {'length': 6}).execute()
    assert len(response.data) == 6
    assert response.data[0]['creation_date'].split('T')[0] == '2024-12-01'
    assert response.data[1]['creation_date'].split('T')[0] == '2024-10-30'
    assert response.data[2]['creation_date'].split('T')[0] == '2024-05-01'
    assert response.data[3]['creation_date'].split('T')[0] == '2024-01-30'
    assert response.data[4]['creation_date'].split('T')[0] == '2023-10-29'
    assert response.data[5]['creation_date'].split('T')[0] == '2023-03-29'

    for post in response.data:
        db_connection.table('Posts_test').delete().eq('id', post['post_id']).execute()

def test_get_empty_posts(db_connection):
    response = db_connection.rpc('get_latest_posts_test', {'length': 5}).execute()
    assert len(response.data) == 0

def test_get_one_post(db_connection,setup_test_data_one_post):
    response = db_connection.rpc('get_latest_posts_test', {'length': 1}).execute()
    assert len(response.data) == 1
    assert response.data[0]['creation_date'].split('T')[0] == '2024-12-01'
    for post in response.data:
        db_connection.table('Posts_test').delete().eq('id', post['post_id']).execute()

def test_get_more_posts_than_existing(db_connection, setup_test_data):
    response = db_connection.rpc('get_latest_posts_test', {'length': 10}).execute()
    assert len(response.data) == 6
    for post in response.data:
        db_connection.table('Posts_test').delete().eq('id', post['post_id']).execute()
