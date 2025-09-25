import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------- Users -------------------
def create_user(email: str, password: str, first_name: str, last_name: str, mobile: str):
    """Signup using Supabase Auth and create user record"""
    auth_res = supabase.auth.sign_up({"email": email, "password": password})
    if auth_res.user:
        supabase.table("users").insert({
            "id": auth_res.user.id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "mobile": mobile
        }).execute()
    return auth_res

def get_user_by_email(email: str):
    """Fetch user by email"""
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data[0] if response.data else None

def update_user(user_id: str, first_name: str = None, last_name: str = None, email: str = None, mobile: str = None):
    """Update user info"""
    updates = {}
    if first_name: updates["first_name"] = first_name
    if last_name: updates["last_name"] = last_name
    if email: updates["email"] = email
    if mobile: updates["mobile"] = mobile
    if updates:
        return supabase.table("users").update(updates).eq("id", user_id).execute()
    return None

def delete_user(user_id: str):
    """Delete user"""
    supabase.auth.api.delete_user(user_id)
    return supabase.table("users").delete().eq("id", user_id).execute()


# ------------------- Recipes -------------------
def create_recipe(user_id: str, data: dict):
    """Add recipe for a user"""
    data["user_id"] = user_id
    return supabase.table("recipes").insert(data).execute()

def get_recipes(user_id: str):
    """Fetch recipes for a user"""
    return supabase.table("recipes").select("*").eq("user_id", user_id).execute().data

def update_recipe(recipe_id: str, data: dict):
    return supabase.table("recipes").update(data).eq("recipe_id", recipe_id).execute()

def delete_recipe(recipe_id: str):
    return supabase.table("recipes").delete().eq("recipe_id", recipe_id).execute()


# ------------------- Saved Recipes -------------------
def save_recipe(user_id: str, recipe_id: str):
    return supabase.table("saved_recipes").insert({
        "user_id": user_id,
        "recipe_id": recipe_id
    }).execute()

def get_saved_recipes(user_id: str):
    return supabase.table("saved_recipes").select("*").eq("user_id", user_id).execute().data