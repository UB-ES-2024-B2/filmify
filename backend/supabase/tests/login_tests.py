import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env file from the parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '../../../.env'))

# Now you can access your environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Contador de aserciones pasadas y fallidas
asserts_passed = 0
asserts_failed = 0
total_asserts = 5  # Cambia este número si agregas más pruebas

# Pruebas

# - Login Exitoso
try:
    responseExitoso = supabase.rpc("login", {"username": "USUARIO_TEST", "input_password": "SecurePassword"}).execute()
    assert responseExitoso.data == [{'signinsuccessful': True, 'errormessage': 'Inicio de sesión correcto.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en inicio de sesión exitoso")

# - Username Vacio
try:
    responseUsernameVacio = supabase.rpc("login", {"username": "", "input_password": "SecurePassword"}).execute()
    assert responseUsernameVacio.data == [{'signinsuccessful': False, 'errormessage': 'Error: El campo username no puede estar vacío.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en username vacío")

# - Password Vacia
try:
    responsePasswordVacio = supabase.rpc("login", {"username": "USUARIO_TEST", "input_password": ""}).execute()
    assert responsePasswordVacio.data == [{'signinsuccessful': False, 'errormessage': 'Error: El campo password no puede estar vacío.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en password vacío")

# - Usuario No Existe
try:
    responseUsuarioNoExiste = supabase.rpc("login", {"username": "UsuarioInexistente", "input_password": "SecurePassword"}).execute()
    assert responseUsuarioNoExiste.data == [{'signinsuccessful': False, 'errormessage': 'Error: El nombre de usuario no existe.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en usuario no existe")

# - Contraseña Incorrecta
try:
    responseContrasenaIncorrecta = supabase.rpc("login", {"username": "USUARIO_TEST", "input_password": "WrongPassword"}).execute()
    assert responseContrasenaIncorrecta.data == [{'signinsuccessful': False, 'errormessage': 'Error: La contraseña no coincide.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en contraseña incorrecta")

# Resultados finales
print(f"Total de aserciones: {total_asserts}, Aserciones pasadas: {asserts_passed}, Aserciones fallidas: {asserts_failed}")
