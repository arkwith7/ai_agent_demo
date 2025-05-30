from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from api.routers.auth import router as auth_router
from api.routers.ai_service import router as ai_service_router

app = FastAPI(
    title="AI Agent Backend",
    description="LangChain + Azure OpenAI 기반 AI Agent 서비스. JWT 인증 및 Swagger 문서화 지원.",
    version="1.0.0",
    contact={
        "name": "AI Agent Demo Team",
        "email": "admin@example.com",
    },
)

# CORS 허용 (프론트엔드와 연동 시 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(ai_service_router, prefix="/ai", tags=["ai"])

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
