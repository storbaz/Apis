from fastapi import APIRouter
from app.api.v1.culture import router as culture_router
from app.api.v1.budget import router as budget_router
from app.api.v1.events import router as events_router
from app.api.v1.transport import router as transport_router
from app.api.v1.food import router as food_router
from app.api.v1.emergency import router as emergency_router
from app.api.v1.auth import router as auth_router
from app.api.v1.favorites import router as favorites_router
from app.api.v1.itineraries import router as itineraries_router
from app.api.v1.weather import router as weather_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(auth_router)
api_router.include_router(favorites_router)
api_router.include_router(itineraries_router)
api_router.include_router(weather_router)
api_router.include_router(culture_router)
api_router.include_router(budget_router)
api_router.include_router(events_router)
api_router.include_router(transport_router)
api_router.include_router(food_router)
api_router.include_router(emergency_router)
