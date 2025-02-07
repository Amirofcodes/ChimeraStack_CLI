from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:8000"]

settings = Settings()