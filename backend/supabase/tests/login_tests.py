from supabase import create_client, Client

SUPABASE_URL = "https://ydzntmbvtktgeknydngv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlkem50bWJ2dGt0Z2Vrbnlkbmd2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkwMTczODcsImV4cCI6MjA0NDU5MzM4N30.eM6tB5yhGYJrVAngp5XPRWmZmpWdAmlAfZ7XlCQV1N4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print(supabase.rpc("login", {"username": "....", "input_password": "test"}).execute())

print(supabase.rpc("login", {"username": "test2", "input_password": "test"}).execute())