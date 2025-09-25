# src/db.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert(table: str, data: dict):
    """Generic insert into any table"""
    try:
        response = supabase.table(table).insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Insert error: {e}")
        return None

def fetch(table: str, filters: dict = None):
    """Generic fetch with optional filters"""
    try:
        query = supabase.table(table).select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Fetch error: {e}")
        return []

def update(table: str, filters: dict, data: dict):
    """Generic update"""
    try:
        query = supabase.table(table).update(data)
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Update error: {e}")
        return None

def delete(table: str, filters: dict):
    """Generic delete"""
    try:
        query = supabase.table(table).delete()
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Delete error: {e}")
        return None