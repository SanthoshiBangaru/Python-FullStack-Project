# src/logic.py

from src.db import (
    create_recipe,
    get_recipes,
    get_all_recipes,
    update_recipe,
    delete_recipe,
    save_recipe,
    get_saved_recipes,
    remove_saved_recipe
)

class RecipeManager:
    """
    Acts as a bridge between frontend (Streamlit/FastAPI) and the recipes database.
    Provides CRUD operations and search functionality.
    """

    def __init__(self, db=None):
        """
        db is optional; if you want, you can pass a custom db object.
        Currently uses imported db functions directly.
        """
        self.db = db

    # ------------------- Recipes CRUD -------------------
    def add_recipe(self, data: dict):
        """Add a new recipe"""
        if not data.get("title") or not data.get("description"):
            return {"success": False, "Message": "Title and Description are required"}
        result = create_recipe(data)
        if result:
            return {"success": True, "Message": "Recipe added successfully", "data": result}
        return {"success": False, "Message": "Failed to add recipe"}

    def fetch_recipes(self, user_id: int = None, title_search: str = None):
        """Fetch recipes by user_id and/or title search"""
        result = get_recipes(user_id=user_id, title_search=title_search)
        return {"success": True, "Message": "Recipes fetched successfully", "data": result}

    def fetch_all_recipes(self):
        """Fetch all recipes"""
        result = get_all_recipes()
        return {"success": True, "Message": "All recipes fetched successfully", "data": result}

    def modify_recipe(self, recipe_id: int, data: dict):
        """Update a recipe by recipe_id"""
        if not data:
            return {"success": False, "Message": "No update data provided"}
        result = update_recipe(recipe_id, data)
        if result:
            return {"success": True, "Message": "Recipe updated successfully", "data": result}
        return {"success": False, "Message": "Recipe not found or update failed"}

    def remove_recipe(self, recipe_id: int):
        """Delete a recipe by recipe_id"""
        result = delete_recipe(recipe_id)
        if result:
            return {"success": True, "Message": "Recipe deleted successfully"}
        return {"success": False, "Message": "Recipe not found or delete failed"}

    # ------------------- Saved Recipes -------------------
    def save_user_recipe(self, user_id: int, recipe_id: int):
        """Save a recipe for a user"""
        result = save_recipe(user_id, recipe_id)
        if result:
            return {"success": True, "Message": "Recipe saved successfully", "data": result}
        return {"success": False, "Message": "Failed to save recipe"}

    def fetch_saved_recipes(self, user_id: int):
        """Get all recipes saved by a user"""
        result = get_saved_recipes(user_id)
        return {"success": True, "Message": "Saved recipes fetched successfully", "data": result}

    # ------------------- Dedicated search -------------------
    def search_recipes_by_title(self, title: str, user_id: int = None):
        """Search recipes by title, optionally filtered by user_id"""
        if not title:
            return {"success": False, "Message": "Search title required"}
        result = get_recipes(user_id=user_id, title_search=title)
        return {"success": True, "Message": f"Recipes matching '{title}' fetched successfully", "data": result}
    
    def unsave_user_recipe(self, user_id: int, recipe_id: int):
        """Remove a saved recipe for the user"""
        return remove_saved_recipe(user_id, recipe_id)  # implement this in db.py