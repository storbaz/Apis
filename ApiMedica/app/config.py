from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Coffee Commodity API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite+aiosqlite:///./coffee_api.db"

    JWT_SECRET: str = "super-secret-change-in-production"
    JWT_EXPIRATION_HOURS: int = 72

    USDA_FAS_API_KEY: str = ""
    FRED_API_KEY: str = ""

    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRO_PRICE_ID: str = ""
    STRIPE_ENTERPRISE_PRICE_ID: str = ""
    FRONTEND_URL: str = "http://localhost:3000"

    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@commoditydata.io"

    POSTHOG_API_KEY: str = ""
    POSTHOG_HOST: str = "https://us.i.posthog.com"

    SENTRY_DSN: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
