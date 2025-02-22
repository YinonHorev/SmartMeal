from fastapi import FastAPI, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from models import Product, UserPreferences, Recipe

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
    # Return a sample recipe using the default values
    return [Recipe()]

@app.get("/products/sponsored", dependencies=[Security(get_api_key)])
async def get_sponsored_products():
    # Return sample products
    return [Product(), Product(id=2, name="Fresh Pasta", promotional=True)]

@app.get("/user/preferences", dependencies=[Security(get_api_key)])
async def get_user_preferences():
    # Return sample user preferences
    return UserPreferences()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
