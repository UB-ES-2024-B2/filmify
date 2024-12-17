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

@pytest.fixture
def setup_db(db_connection):
    db_connection.table("Usuarios").insert([{"username": "USUARIO_TEST", "password": "SecurePassword", "s_email": "newuser@example.com"}])

@pytest.fixture
def empty_db(db_connection):
    db_connection.table("Usuarios").delete().eq('user_name', 'USUARIO_TEST').execute()

def test_create_user(db_connection, empty_db):
    responseExitoso = db_connection.rpc("register_user", {"username": "USUARIO_TEST", "password": "SecurePassword", "s_email": "newuser@example.com"}).execute()
    assert responseExitoso.data == [{'signupsuccessful': True, 'errormessage': 'Usuario creado exitosamente.'}]

def test_invalid_username(db_connection):
    responseUsernameVacio = db_connection.rpc("register_user", {"username": "", "password": "SecurePassword", "s_email": "anotheruser@example.com"}).execute()
    assert responseUsernameVacio.data == [{'signupsuccessful': False, 'errormessage': 'Error: El campo username no puede estar vacío.'}]

# - Password Vacia
def test_invalid_password(db_connection):
    responsePasswordVacio = db_connection.rpc("register_user", {"username": "AnotherUser", "password": "", "s_email": "anotheruser@example.com"}).execute()
    assert responsePasswordVacio.data == [{'signupsuccessful': False, 'errormessage': 'Error: El campo password no puede estar vacío.'}]

def test_invalid_email(db_connection):
    responseMailVacio = db_connection.rpc("register_user", {"username": "AnotherUser", "password": "SecurePassword", "s_email": ""}).execute()
    assert responseMailVacio.data == [{'signupsuccessful': False, 'errormessage': 'Error: El campo email no puede estar vacío.'}]

def test_existing_username(db_connection, setup_db):
    responseUsuarioEnUso = db_connection.rpc("register_user", {"username": "USUARIO_TEST", "password": "AnotherPassword", "s_email": "anotheruser@example.com"}).execute()
    assert responseUsuarioEnUso.data == [{'signupsuccessful': False, 'errormessage': 'Error: El nombre de usuario ya está en uso.'}]

def test_existing_email(db_connection, setup_db):
    responseCorreoRegistrado = db_connection.rpc("register_user", {"username": "AnotherUser", "password": "AnotherPassword", "s_email": "newuser@example.com"}).execute()
    assert responseCorreoRegistrado.data == [{'signupsuccessful': False, 'errormessage': 'Error: La dirección de correo ya está registrada.'}]


