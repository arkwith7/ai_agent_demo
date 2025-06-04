from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from api.routers.analysis import router as analysis_router # 주식 분석 및 추천 관련 API
from api.routers.chat import router as chat_router       # 채팅 관련 API
from api.routers.auth import router as auth_router       # 사용자 인증 API
from api.routers.user_management import router as user_router # 사용자 관리 API
from core.config import settings
from db.init_db import init_models

app = FastAPI(
    title="AI Stock Analysis API",
    description="AI 기반 주식 분석 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(analysis_router, prefix="/api/analysis", tags=["analysis"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(user_router, prefix="/api", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Stock Analysis API"}

# Database initialization on startup
@app.on_event("startup")
async def startup_event():
    await init_models()

# Swagger UI에서 JWT 인증 헤더 입력 지원
# (FastAPI 공식 문서 참고)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
