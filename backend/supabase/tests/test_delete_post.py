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

title_test = 'g>rUAl!q.f?>xsQ3T]Va'
content_test = '_26I*UP5k=UA]e%IW7?'

# Create Post
def test_post_create(db_connection):
    response = db_connection.rpc("create_post", {'title': title_test, 'content': content_test, 'input_movie_id': 12, 'user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert response.data

post_id_test = None

# Comprobación de que se ha creado el post
def test_post_get(db_connection):
    response = db_connection.rpc("get_posts", {'input_movie_id': 12}).execute()
    exist_post = False
    for post in response.data:
        if post['title'] == title_test and post['content'] == content_test:
            exist_post = True
            post_id_test = post['post_id']
    assert exist_post == True

# Delete Post con post_id que no existe
def test_post_delete1(db_connection):
    response = db_connection.rpc("delete_post_by_id", {'input_post_id': 99999 ,'input_user_id': '8a30b414-3548-0000-98de-1f849a77ef81'}).execute()
    assert response.data == False

# Delete Post con un user_id que no es el del autor
def test_post_delete2(db_connection):
    response = db_connection.rpc("delete_post_by_id", {'input_post_id': 40 ,'input_user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022c'}).execute()
    assert response.data == False

# Delete Post 
def test_post_delete3(db_connection):
    response = db_connection.rpc("get_posts", {'input_movie_id': 12}).execute()
    post_id_test = None
    for post in response.data:
        if post['title'] == title_test and post['content'] == content_test:
            post_id_test = post['post_id']
    response2 = db_connection.rpc("delete_post_by_id", {'input_post_id': post_id_test ,'input_user_id': '8a30b414-3548-434a-98de-1f849a77ef81'}).execute()
    assert response2.data == True

# Comprobación de que se ha eliminado el post
def test_post_get2(db_connection):
    response = db_connection.rpc("get_posts", {'input_movie_id': 12}).execute()
    exist_post = False
    for post in response.data:
        if post['title'] == title_test and post['content'] == content_test:
            exist_post = True
            post_id_test = post['post_id']
    assert exist_post == False
