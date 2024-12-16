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

def test_top5posts(db_connection):
    response = db_connection.rpc("get_top_posts", {'length': 5}).execute()
    assert len(response.data) == 5