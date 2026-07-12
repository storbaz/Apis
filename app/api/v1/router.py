from fastapi import APIRouter
from app.api.v1.maps import router as maps_router
from app.api.v1.health import router as health_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(maps_router)
api_router.include_router(health_router)
