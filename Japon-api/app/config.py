from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    APP_NAME: str = "Japan Travel API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "change-this-in-production"
    ALLOWED_ORIGINS: list[str] = [
        "https://www.viajapp.app",
        "https://japan-travel-web.vercel.app",
        "https://viajapp.app",
        "https://www.viajapp.app",
        "http://localhost:3000",
    ]

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    FREE_TIER_DAILY_LIMIT: int = 100
    PREMIUM_TIER_DAILY_LIMIT: int = 10000

    SERPER_API_KEY: str = ""
    OPENWEATHER_API_KEY: str = ""

    @property
    def is_secret_key_valid(self) -> bool:
        return len(self.SECRET_KEY) >= 32 and self.SECRET_KEY != "change-this-in-production"

settings = Settings()