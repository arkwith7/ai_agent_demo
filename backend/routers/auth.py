from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()

@router.post("/login")
async def login(email: str, password: str):
    """사용자 로그인을 처리합니다."""
    try:
        # 임시로 항상 성공 반환
        return {
            "access_token": "dummy_token",
            "refresh_token": "dummy_refresh_token"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")
async def register(user_data: Dict[str, Any]):
    """사용자 등록을 처리합니다."""
    try:
        # 임시로 항상 성공 반환
        return {
            "message": "회원가입이 완료되었습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """토큰 갱신을 처리합니다."""
    try:
        # 임시로 항상 성공 반환
        return {
            "access_token": "new_dummy_token"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 