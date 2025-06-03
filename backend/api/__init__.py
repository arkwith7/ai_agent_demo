# API package

from fastapi import APIRouter
from .routers import ai_service, auth, user_management, chat_message

api_router = APIRouter()

# 인증 관련 라우터
api_router.include_router(auth.router, prefix="/auth", tags=["인증"])

# 사용자 관리 라우터
api_router.include_router(user_management.router, prefix="/users", tags=["사용자 관리"])

# 채팅 메시지 라우터
api_router.include_router(chat_message.router, prefix="/chat", tags=["채팅"])

# AI 서비스 라우터
api_router.include_router(ai_service.router, prefix="/ai", tags=["AI 서비스"])
