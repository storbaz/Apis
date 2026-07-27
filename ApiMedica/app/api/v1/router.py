from fastapi import APIRouter

from app.api.v1.production import router as production_router
from app.api.v1.prices import router as prices_router
from app.api.v1.exports import router as exports_router
from app.api.v1.imports import router as imports_router
from app.api.v1.auth import router as auth_router
from app.api.v1.api_keys import router as api_keys_router
from app.api.v1.billing import router as billing_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(auth_router)
api_router.include_router(api_keys_router)
api_router.include_router(billing_router)
api_router.include_router(production_router, tags=["production"])
api_router.include_router(prices_router, tags=["prices"])
api_router.include_router(exports_router, tags=["exports"])
api_router.include_router(imports_router, tags=["imports"])
