from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from functools import lru_cache
from dotenv import load_dotenv
import os

# backend 디렉토리의 .env 파일 로드
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

class Settings(BaseSettings):
    # 프로젝트 기본 설정
    PROJECT_NAME: str = "Stock Analysis API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///./stock_analysis.db"
    
    # JWT 설정
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OpenAI API 설정
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    OPENAI_API_VERSION: str
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: str
    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME: str
    
    # 금융위원회 API 설정
    FSS_API_KEY: str
    
    # OpenDART API 설정
    OPEN_DART_API_KEY: str
    
    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        case_sensitive = True
        extra = "ignore"  # 추가 필드 무시

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
