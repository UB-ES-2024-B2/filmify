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

def test_login(db_connection):
    responseExitoso = db_connection.rpc("login", {"username": "USUARIO_TEST", "input_password": "SecurePassword"}).execute()
    assert responseExitoso.data == [{'signinsuccessful': True, 'errormessage': 'Inicio de sesión correcto.'}]

def test_empty_username(db_connection):
    responseUsernameVacio = db_connection.rpc("login", {"username": "", "input_password": "SecurePassword"}).execute()
    assert responseUsernameVacio.data == [{'signinsuccessful': False, 'errormessage': 'Error: El campo username no puede estar vacío.'}]

def test_empty_password(db_connection):
    responsePasswordVacio = db_connection.rpc("login", {"username": "USUARIO_TEST", "input_password": ""}).execute()
    assert responsePasswordVacio.data == [{'signinsuccessful': False, 'errormessage': 'Error: El campo password no puede estar vacío.'}]

def test_no_existing_username(db_connection):
    responseUsuarioNoExiste = db_connection.rpc("login", {"username": "UsuarioInexistente", "input_password": "SecurePassword"}).execute()
    assert responseUsuarioNoExiste.data == [{'signinsuccessful': False, 'errormessage': 'Error: El nombre de usuario no existe.'}]

def test_incorrect_password(db_connection):
    responseContrasenaIncorrecta = db_connection.rpc("login", {"username": "USUARIO_TEST", "input_password": "WrongPassword"}).execute()
    assert responseContrasenaIncorrecta.data == [{'signinsuccessful': False, 'errormessage': 'Error: La contraseña no coincide.'}]

