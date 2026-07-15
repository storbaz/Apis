from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    import httpx

    async def keep_alive():
        while True:
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    await client.get("https://apis-4g3r.onrender.com/")
            except Exception:
                pass
            await asyncio.sleep(480)

    asyncio.create_task(keep_alive())
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="API for generating business leads from Google Maps with email enrichment",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
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
            "docs": "/docs"
        }

    return app


app = create_app()
