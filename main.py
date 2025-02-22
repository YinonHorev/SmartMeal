import logging
from fastapi import FastAPI, Security, HTTPException, Header, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
from models import Product, UserPreferences, Recipe, GenerateRecipeRequest
from openai import OpenAI, OpenAIError
from db import RecipeDB

recipe_db = RecipeDB()

API_KEY = "default_api_key_12345"
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI()

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header and api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate API key"
    )

@app.get("/", dependencies=[Security(get_api_key)])
async def root():
    return {"message": "Hello, World!"}

@app.get("/recipes/recommended", dependencies=[Security(get_api_key)])
async def get_recommended_recipes():
    return recipe_db.get_recipes()

@app.get("/products/sponsored", dependencies=[Security(get_api_key)])
async def get_sponsored_products():
    # Return sample products
    return [Product(), Product(id=2, name="Fresh Pasta", promotional=True)]

@app.get("/user/preferences", dependencies=[Security(get_api_key)])
async def get_user_preferences():
    # Return sample user preferences
    return UserPreferences()

async def get_openai_client(open_ai_token: str = Header(...)) -> OpenAI:
    return OpenAI(api_key=open_ai_token)

@app.post("/recipes/generate", dependencies=[Security(get_api_key)])
async def generate_recipe(
    request: GenerateRecipeRequest,
    client: OpenAI = Depends(get_openai_client)
):
    try:
        # Create the prompt for recipe generation
        prompt = f"Generate a recipe for: {request.prompt}\n"
        prompt += "Include title, ingredients, preparation time, difficulty, and instructions."

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            store=False,
            messages=[
                {"role": "system", "content": "You are a professional chef creating detailed recipes."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the recipe text from the response
        recipe_text = completion.choices[0].message

        # For now, return a basic Recipe with some fields from GPT
        # In a real implementation, you'd want to parse the GPT response more carefully
        recipe = Recipe(
            prompt=request.prompt,
            title=request.prompt.title(),
            ingredients=["Generated ingredients will go here"],
            preparation_time=30,
            difficulty="medium",
            nutritional_info="Generated nutritional info",
            instructions=recipe_text.content.split("\n")
        )
        recipe_db.add_recipe(recipe)
        return recipe

    except OpenAIError as e:
        logging.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recipe"
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
