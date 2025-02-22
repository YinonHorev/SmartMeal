import json
from pathlib import Path
from typing import List
from models import Recipe

class RecipeDB:
    def __init__(self, file_path: str = "recipes.json"):
        self.file_path = Path(file_path)
        self.recipes: List[Recipe] = []
        self._load_recipes()

    def _load_recipes(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.recipes = [Recipe(**recipe) for recipe in data]

    def save_recipes(self):
        with open(self.file_path, 'w') as f:
            json.dump([recipe.model_dump() for recipe in self.recipes], f, indent=2)

    def add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)
        self.save_recipes()

    def get_recipes(self) -> List[Recipe]:
        return self.recipes
