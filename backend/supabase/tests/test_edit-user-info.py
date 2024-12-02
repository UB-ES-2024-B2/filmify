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


def test_updateUsername(db_connection):
    response = db_connection.rpc('edituserinfo', {'userid':'f3cf42e6-6380-4ed7-95c0-05eceae1022c', 'username':'eshaanmittal', 'userbio':''}).execute()
    assert response.data == [{'changesuccessful': True, 'errormessage': 'Changes applied successfully'}]

def test_updateBio(db_connection):
    response = db_connection.rpc('edituserinfo', {'userid':'f3cf42e6-6380-4ed7-95c0-05eceae1022c', 'username':'', 'userbio':'Hello, I am Eshaan!'}).execute()
    assert response.data == [{'changesuccessful': True, 'errormessage': 'Changes applied successfully'}]

def test_updateBoth(db_connection):
    response = db_connection.rpc('edituserinfo', {'userid':'f3cf42e6-6380-4ed7-95c0-05eceae1022c', 'username':'em1ttal', 'userbio':'This is a test.'}).execute()
    assert response.data == [{'changesuccessful': True, 'errormessage': 'Changes applied successfully'}]

def test_noUpdateDone(db_connection):
    response = db_connection.rpc('edituserinfo', {'userid':'f3cf42e6-6380-4ed7-95c0-05eceae1022c', 'username':'', 'userbio':''}).execute()
    assert response.data == [{'changesuccessful': False, 'errormessage': 'No valid parameters provided or no changes applied'}]

def test_incorrectUserID(db_connection):
    response = db_connection.rpc('edituserinfo', {'userid':'f3cf42e6-8380-4ed7-95c0-15eceae1025c', 'username':'', 'userbio':''}).execute()
    assert response.data == [{'changesuccessful': False, 'errormessage': 'No valid parameters provided or no changes applied'}]

