import bcrypt
from src.db import insert, fetch, update, delete

# ---------- User Authentication ----------
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def signup_user(first_name: str, last_name: str, email: str, mobile: str, password: str):
    """Register a new user"""
    if fetch("users", {"email": email}):
        raise ValueError("Email already registered")
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "mobile": mobile,
        "password_hash": hash_password(password)
    }
    return insert("users", data)

def login_user(email: str, password: str):
    """Login user with email and password"""
    users = fetch("users", {"email": email})
    if not users:
        return None
    user = users[0]
    if check_password(password, user["password_hash"]):
        return {
            "user_id": user["user_id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"]
        }
    return None

# ---------- Recipes CRUD ----------
def create_recipe(user_id: int, title: str, description: str, instructions: str = "", image_url: str = "", prep_time: str = "", ingredients: str = "", allergens: str = ""):
    """Create a new recipe for a user"""
    data = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "instructions": instructions,
        "image_url": image_url,
        "prep_time": prep_time,
        "ingredients": ingredients,
        "allergens": allergens,
        "source": "Custom"
    }
    return insert("recipes", data)

def get_recipes(user_id: int):
    return fetch("recipes", {"user_id": user_id})

def update_recipe(recipe_id: int, updates: dict):
    return update("recipes", {"recipe_id": recipe_id}, updates)

def delete_recipe(recipe_id: int):
    return delete("recipes", {"recipe_id": recipe_id})

# ---------- Saved Recipes ----------
def save_recipe(user_id: int, recipe_id: int):
    return insert("saved_recipes", {"user_id": user_id, "recipe_id": recipe_id})

def get_saved_recipes(user_id: int):
    return fetch("saved_recipes", {"user_id": user_id})