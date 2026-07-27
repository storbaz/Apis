from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="API completa para viajeros a Japon",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "endpoints": {
                "auth": "/v1/auth",
                "culture": "/v1/culture",
                "budget": "/v1/budget",
                "events": "/v1/events",
                "transport": "/v1/transport",
                "food": "/v1/food",
                "emergency": "/v1/emergency",
                "weather": "/v1/weather",
                "favorites": "/v1/favorites",
                "itineraries": "/v1/itineraries",
            }
        }

    return app


app = create_app()
