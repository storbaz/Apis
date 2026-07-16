from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    APP_NAME: str = "Japan Travel API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "change-this-in-production"
    ALLOWED_ORIGINS: list[str] = ["*"]

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    FREE_TIER_DAILY_LIMIT: int = 100
    PREMIUM_TIER_DAILY_LIMIT: int = 10000

settings = Settings()