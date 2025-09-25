#main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from src.logic import create_recipe, get_recipes, update_recipe, delete_recipe

app = FastAPI(title="Recipe Finder API")

# -------------------------
# Pydantic Models
# -------------------------
class RecipeCreate(BaseModel):
    user_id: int
    title: str
    description: str
    instructions: Optional[str] = None

class RecipeUpdate(BaseModel):
    updates: Dict[str, str]  # keys: 'title', 'description', 'instructions'

# -------------------------
# API Endpoints
# -------------------------
@app.post("/recipes/", response_model=dict)
def add_recipe(recipe: RecipeCreate):
    try:
        new_recipe = create_recipe(
            recipe.user_id,
            recipe.title,
            recipe.description,
            recipe.instructions
        )
        return {"status": "success", "recipe": new_recipe}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/recipes/{user_id}", response_model=List[dict])
def list_recipes(user_id: int):
    try:
        recipes = get_recipes(user_id)
        return recipes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/recipes/{recipe_id}", response_model=dict)
def modify_recipe(recipe_id: int, recipe_update: RecipeUpdate):
    try:
        updated_recipe = update_recipe(recipe_id, recipe_update.updates)
        return {"status": "success", "recipe": updated_recipe}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/recipes/{recipe_id}", response_model=dict)
def remove_recipe(recipe_id: int):
    try:
        delete_recipe(recipe_id)
        return {"status": "success", "message": "Recipe deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))