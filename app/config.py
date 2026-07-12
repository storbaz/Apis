from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    SERPER_API_KEY: str = ""
    RAPIDAPI_PROXY_SECRET: str = ""
    EMAIL_VERIFY_TIMEOUT: int = 10
    EMAIL_VERIFY_DELAY: float = 1.0
    APP_NAME: str = "LeadGen API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False


settings = Settings()
