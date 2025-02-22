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

class Recipe(BaseModel):
    title: str = "Classic Margherita Pizza"
    ingredients: List[str] = [
        "2 cups flour",
        "1 cup water",
        "2 tbsp olive oil",
        "Fresh mozzarella",
        "Fresh basil"
    ]

class GenerateRecipeRequest(BaseModel):
    prompt: str = Field(..., description="Description of the recipe to generate")
    preparation_time: int = 45  # minutes
    difficulty: str = "medium"
    nutritional_info: str = "Calories: 250, Protein: 10g, Carbs: 30g"
    instructions: List[str] = [
        "Prepare the dough",
        "Let it rise for 30 minutes",
        "Add toppings",
        "Bake at 450°F for 15 minutes"
    ]
