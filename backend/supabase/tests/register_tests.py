from supabase import create_client, Client

SUPABASE_URL = "https://ydzntmbvtktgeknydngv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlkem50bWJ2dGt0Z2Vrbnlkbmd2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkwMTczODcsImV4cCI6MjA0NDU5MzM4N30.eM6tB5yhGYJrVAngp5XPRWmZmpWdAmlAfZ7XlCQV1N4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Contador de aserciones pasadas y fallidas
asserts_passed = 0
asserts_failed = 0
total_asserts = 6  # Cambia este número si agregas más pruebas

# Pruebas

# - Register Exitoso
try:
    responseExitoso = supabase.rpc("register_user", {"username": "USUARIO_TEST", "password": "SecurePassword", "s_email": "newuser@example.com"}).execute()
    assert responseExitoso.data == [{'signupsuccessful': True, 'errormessage': 'Usuario creado exitosamente.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en registro exitoso")

# - Username Vacio
try:
    responseUsernameVacio = supabase.rpc("register_user", {"username": "", "password": "SecurePassword", "s_email": "anotheruser@example.com"}).execute()
    assert responseUsernameVacio.data == [{'signupsuccessful': False, 'errormessage': 'Error: El campo username no puede estar vacío.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en username vacío")

# - Password Vacia
try:
    responsePasswordVacio = supabase.rpc("register_user", {"username": "AnotherUser", "password": "", "s_email": "anotheruser@example.com"}).execute()
    assert responsePasswordVacio.data == [{'signupsuccessful': False, 'errormessage': 'Error: El campo password no puede estar vacío.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en password vacío")

# - Mail vacio
try:
    responseMailVacio = supabase.rpc("register_user", {"username": "AnotherUser", "password": "SecurePassword", "s_email": ""}).execute()
    assert responseMailVacio.data == [{'signupsuccessful': False, 'errormessage': 'Error: El campo email no puede estar vacío.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en email vacío")

# - Usuario En Uso
try:
    responseUsuarioEnUso = supabase.rpc("register_user", {"username": "USUARIO_TEST", "password": "AnotherPassword", "s_email": "anotheruser@example.com"}).execute()
    assert responseUsuarioEnUso.data == [{'signupsuccessful': False, 'errormessage': 'Error: El nombre de usuario ya está en uso.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en usuario ya en uso")

# - Correo en Uso
try:
    responseCorreoRegistrado = supabase.rpc("register_user", {"username": "AnotherUser", "password": "AnotherPassword", "s_email": "newuser@example.com"}).execute()
    assert responseCorreoRegistrado.data == [{'signupsuccessful': False, 'errormessage': 'Error: La dirección de correo ya está registrada.'}]
    asserts_passed += 1
except AssertionError:
    asserts_failed += 1
    print("Fallo en correo ya registrado")

# Resultados finales
print(f"Total de aserciones: {total_asserts}, Aserciones pasadas: {asserts_passed}, Aserciones fallidas: {asserts_failed}")
