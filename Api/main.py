from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, List
from src.logic import RecipeManager

app = FastAPI(title="Recipe Finder API")
manager = RecipeManager()  # Initialize the RecipeManager

# ---------- Models ----------
class RecipeCreate(BaseModel):
    user_id: int
    title: str
    description: str
    instructions: Optional[str] = None
    ingredients: Optional[str] = None
    prep_time: Optional[str] = None
    image_url: Optional[str] = None

class RecipeUpdate(BaseModel):
    updates: Dict[str, str]

# ---------- Endpoints ----------

@app.post("/recipes/", response_model=dict)
def create_new_recipe(recipe: RecipeCreate):
    result = manager.add_recipe(recipe.dict())
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["Message"])
    return result

@app.get("/recipes/", response_model=dict)
def list_recipes(user_id: Optional[int] = None, title: Optional[str] = Query(None, description="Search by recipe title")):
    if title:
        result = manager.search_recipes_by_title(title, user_id=user_id)
    elif user_id:
        result = manager.fetch_recipes(user_id=user_id)
    else:
        result = manager.fetch_all_recipes()
    return result

@app.put("/recipes/{recipe_id}", response_model=dict)
def update_existing_recipe(recipe_id: int, recipe_update: RecipeUpdate):
    result = manager.modify_recipe(recipe_id, recipe_update.updates)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["Message"])
    return result

@app.delete("/recipes/{recipe_id}", response_model=dict)
def delete_existing_recipe(recipe_id: int):
    result = manager.remove_recipe(recipe_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["Message"])
    return result