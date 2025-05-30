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
    
    # External API Keys for enhanced analysis
    OPEN_DART_API_KEY: str | None = None
    KRX_API_KEY: str | None = None

    # OpenAI & LLM
    OPENAI_API_KEY: str | None = None
    LLM_PROVIDER: str | None = None
    TEMPERATURE: float | None = None
    AZURE_OPENAI_KEY: str | None = None
    AZURE_OPENAI_API_VERSION: str | None = None
    AZURE_OPENAI_DEPLOYMENT_NAME: str | None = None
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str | None = None
    AZURE_OPENAI_EMBEDDING_DIMENSIONS: int | None = None
    # Azure Search
    AZURE_SEARCH_SERVICE_ENDPOINT: str | None = None
    AZURE_SEARCH_ADMIN_KEY: str | None = None
    AZURE_SEARCH_INDEX: str | None = None
    AZURE_SEARCH_DATASOURCE: str | None = None
    # Azure Blob
    AZURE_BLOB_CONNECTION_STRING: str | None = None
    AZURE_BLOB_CONTAINER_NAME: str | None = None
    AZURE_BLOB_ACCOUNT_URL: str | None = None
    # Azure Document Intelligence
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: str | None = None
    AZURE_DOCUMENT_INTELLIGENCE_KEY: str | None = None
    # Redis
    REDIS_HOST: str | None = None
    REDIS_PORT: int | None = None
    # DB
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None
    # 논문 특허 API
    DBPIA_API_KEY: str | None = None

    class Config:
        env_file = "backend/.env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
