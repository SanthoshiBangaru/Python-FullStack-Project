import os
from dotenv import load_dotenv
from supabase import create_client, Client

# ------------------- Setup -------------------
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
    if getattr(auth_res, "user", None):
        # Insert into users table (store Auth UUID in auth_id)
        supabase.table("users").insert({
            "auth_id": auth_res.user.id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "mobile": mobile,
            "password_hash": ""  # optional if using Auth only
        }).execute()
    return auth_res

def get_user_by_email(email: str):
    """Fetch user by email"""
    response = supabase.table("users").select("*").eq("email", email).execute()
    return getattr(response, "data", [None])[0]

def update_user(user_id: int, first_name: str = None, last_name: str = None, email: str = None, mobile: str = None):
    """Update user info"""
    updates = {}
    if first_name: updates["first_name"] = first_name
    if last_name: updates["last_name"] = last_name
    if email: updates["email"] = email
    if mobile: updates["mobile"] = mobile
    if updates:
        response = supabase.table("users").update(updates).eq("user_id", user_id).execute()
        return getattr(response, "data", [])
    return None

def delete_user(user_id: int):
    """Delete user from Auth and table"""
    user = supabase.table("users").select("*").eq("user_id", user_id).execute().data
    if user:
        auth_id = user[0].get("auth_id")
        if auth_id:
            supabase.auth.admin.delete_user(auth_id)
        response = supabase.table("users").delete().eq("user_id", user_id).execute()
        return getattr(response, "data", [])
    return None

# ------------------- Recipes -------------------
def create_recipe(data: dict):
    """Add a recipe (user_id optional if no login)"""
    response = supabase.table("recipes").insert(data).execute()
    return getattr(response, "data", [])

def get_recipes(user_id: int = None, title_search: str = None):
    """Fetch recipes, optionally filter by user_id or title substring"""
    query = supabase.table("recipes").select("*")
    if user_id:
        query = query.eq("user_id", user_id)
    if title_search:
        query = query.ilike("title", f"%{title_search}%")
    response = query.execute()
    return getattr(response, "data", [])

def get_all_recipes():
    """Fetch all recipes"""
    response = supabase.table("recipes").select("*").execute()
    return getattr(response, "data", [])

def update_recipe(recipe_id: int, data: dict):
    """Update recipe by recipe_id"""
    response = supabase.table("recipes").update(data).eq("recipe_id", recipe_id).execute()
    return getattr(response, "data", [])

def delete_recipe(recipe_id: int):
    """Delete recipe by recipe_id"""
    response = supabase.table("recipes").delete().eq("recipe_id", recipe_id).execute()
    return getattr(response, "data", [])

# ------------------- Saved Recipes -------------------
def save_recipe(user_id: int, recipe_id: int):
    """Save a recipe for a user"""
    response = supabase.table("saved_recipes").insert({
        "user_id": user_id,
        "recipe_id": recipe_id
    }).execute()
    return getattr(response, "data", [])

def get_saved_recipes(user_id: int):
    """Get all recipes saved by a user"""
    response = supabase.table("saved_recipes").select("*").eq("user_id", user_id).execute()
    return getattr(response, "data", [])

def remove_saved_recipe(user_id: int, recipe_id: int):
    return supabase.table("saved_recipes").delete().eq("user_id", user_id).eq("recipe_id", recipe_id).execute()

# ------------------- Debug Helper -------------------
def print_all_recipes():
    """Utility to print all recipes"""
    recipes = get_all_recipes()
    if not recipes:
        print("No recipes found.")
    else:
        for r in recipes:
            print(f"{r['recipe_id']}: {r.get('title', '')} by User {r.get('user_id')}")