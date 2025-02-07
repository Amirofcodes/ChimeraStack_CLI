import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    PROJECT_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    DATABASE_URL: str = f"sqlite:///{PROJECT_DIR}/data/app.db"

@lru_cache()
def get_settings():
    return AppSettings()