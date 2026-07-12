from fastapi import Header, HTTPException
from app.config import settings


async def verify_rapidapi_key(x_rapidapi_proxy_secret: str = Header(default="")):
    if settings.RAPIDAPI_PROXY_SECRET and x_rapidapi_proxy_secret != settings.RAPIDAPI_PROXY_SECRET:
        raise HTTPException(status_code=401, detail="Invalid API key")


async def get_api_key(x_rapidapi_key: str = Header(default="")):
    if not x_rapidapi_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    return x_rapidapi_key
