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


# - Test Posts Sorted By Score
def test_posts_sorted(db_connection):
    response = db_connection.rpc("get_posts", {'input_movie_id': 12}).execute()
    is_sorted = True
    score = response.data[0]['votes']
    for post in response.data:
        if score < post['votes']:
            is_sorted = False
        score = post['votes']
    assert is_sorted == True