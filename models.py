from typing import List, Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int = 1
    name: str = "Organic Tomatoes"
    promotional: bool = False

class UserPreferences(BaseModel):
    user_id: int = 1
    dietary_restrictions: List[str] = ["vegetarian", "gluten-free"]
    favorite_cuisines: List[str] = ["Italian", "Japanese", "Mexican"]

class GenerateRecipeRequest(BaseModel):
    prompt: str = Field(..., description="Description of the recipe to generate")

class Recipe(BaseModel):
    prompt: str
    title: str
    ingredients: List[str]
    preparation_time: int
    difficulty: str
    nutritional_info: str
    instructions: List[str]
