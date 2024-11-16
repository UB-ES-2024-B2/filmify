import os
import uuid
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
total_asserts = 2  # Cambia este número si agregas más pruebas

# Como solo implementamos que se muestren las peliculas, hemos creado algunas relaciones ya en la base de datos.
# En el siguente sprint implementaremos la funcionalidad que queda.

# Usuario con Wishlist
try:
    response = supabase.rpc("get_wishlist", {'user_id': 'f3cf42e6-6380-4ed7-95c0-05eceae1022c'}).execute()
    assert response.data == [{'id': 12, 'title': 'Buscando a Nemo', 'poster_url': 'https://image.tmdb.org/t/p/original/jPhak722pNGxQIXSEfeWIUqBrO5.jpg', 'vote_average': 7.819, 'vote_count': 19117}, {'id': 24, 'title': 'Kill Bill: Volumen 1', 'poster_url': 'https://image.tmdb.org/t/p/original/lfj709InbmljVqAXgUk2qjnujNN.jpg', 'vote_average': 7.971, 'vote_count': 17257}]
    asserts_passed +=1
except AssertionError:
    asserts_failed +=1

# Usuario sin Wishlist
try:
    response = supabase.rpc("get_wishlist", {'user_id': '1f874ad7-1203-4d6b-bade-73b76582b7e7'}).execute()
    assert response.data == []
    asserts_passed +=1
except AssertionError:
    asserts_failed +=1

# Resultados finales
print(f"Total de aserciones: {total_asserts}, Aserciones pasadas: {asserts_passed}, Aserciones fallidas: {asserts_failed}")