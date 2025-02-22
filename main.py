from fastapi import FastAPI, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
