from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Agent Backend"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    OPENAI_API_VERSION: str = "2023-12-01-preview"
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: str
    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
