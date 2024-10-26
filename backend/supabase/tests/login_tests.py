from supabase import create_client, Client

SUPABASE_URL = "https://ydzntmbvtktgeknydngv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlkem50bWJ2dGt0Z2Vrbnlkbmd2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkwMTczODcsImV4cCI6MjA0NDU5MzM4N30.eM6tB5yhGYJrVAngp5XPRWmZmpWdAmlAfZ7XlCQV1N4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Contador de aserciones pasadas y fallidas
asserts_passed = 0
asserts_failed = 0
total_asserts = 5  # Cambia este número si agregas más pruebas

# Pruebas

# - Login Exitoso
try:
    responseExitoso = supabase.rpc("login", {"username": "USUARIO_TEST", "input_password": "SecurePassword"}).execute()
    assert responseExitoso.data == [{'signinSuccessful': True, 'errorMessage': 'Inicio de sesión correcto.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en inicio de sesión exitoso")

# - Username Vacio
try:
    responseUsernameVacio = supabase.rpc("login", {"username": "", "input_password": "SecurePassword"}).execute()
    assert responseUsernameVacio.data == [{'signinSuccessful': False, 'errorMessage': 'Error: El campo username no puede estar vacío.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en username vacío")

# - Password Vacia
try:
    responsePasswordVacio = supabase.rpc("login", {"username": "USUARIO_TEST", "input_password": ""}).execute()
    assert responsePasswordVacio.data == [{'signinSuccessful': False, 'errorMessage': 'Error: El campo password no puede estar vacío.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en password vacío")

# - Usuario No Existe
try:
    responseUsuarioNoExiste = supabase.rpc("login", {"username": "UsuarioInexistente", "input_password": "SecurePassword"}).execute()
    assert responseUsuarioNoExiste.data == [{'signinSuccessful': False, 'errorMessage': 'Error: El nombre de usuario no existe.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en usuario no existe")

# - Contraseña Incorrecta
try:
    responseContrasenaIncorrecta = supabase.rpc("login", {"username": "USUARIO_TEST", "input_password": "WrongPassword"}).execute()
    assert responseContrasenaIncorrecta.data == [{'signinSuccessful': False, 'errorMessage': 'Error: La contraseña no coincide.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en contraseña incorrecta")

# Resultados finales
print(f"Total de aserciones: {total_asserts}, Aserciones pasadas: {asserts_passed}, Aserciones fallidas: {asserts_failed}")
