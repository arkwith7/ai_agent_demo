# API 라우터: 인증 및 토큰 관련 엔드포인트
# - POST /api/auth/register: 사용자 회원가입
# - POST /api/auth/login: JWT 토큰 발급
# - POST /api/auth/refresh: 토큰 갱신

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserRead
from schemas.token import Token
from core.security import verify_password, create_access_token, create_refresh_token
from db.session import get_db
from api.routers.crud import crud_user
from db.models.user import UserRole
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/register", response_model=UserRead, summary="사용자 회원가입")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    새로운 사용자 회원가입
    기본적으로 일반 사용자(USER) 권한으로 생성됨
    """
    db_user = await crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = await crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 회원가입 시에는 항상 일반 사용자로 생성 (보안상 이유)
    user.role = UserRole.USER
    
    user_obj = await crud_user.create_user(db, user)
    return UserRead.model_validate(user_obj)

@router.post("/login", response_model=Token, summary="사용자 로그인")
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    사용자 로그인 및 JWT 토큰 발급
    """
    user = await crud_user.get_user_by_email(db, email=login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(
        data={
            "sub": user.email,  # username 대신 email 사용
            "user_id": user.id,
            "role": user.role.value
        }
    )
    refresh_token = create_refresh_token(
        data={
            "sub": user.email,  # username 대신 email 사용
            "user_id": user.id,
            "role": user.role.value
        }
    )
    
    return Token(
        access_token=access_token, 
        refresh_token=refresh_token, 
        token_type="bearer"
    )

@router.post("/refresh", response_model=Token, summary="토큰 갱신")
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """
    Refresh token을 사용하여 새로운 access token 발급
    """
    from core.security import decode_token
    payload = decode_token(request.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid refresh token"
        )
    
    user = await crud_user.get_user_by_email(db, email=payload.get("sub"))  # username 대신 email 사용
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(
        data={
            "sub": user.email,  # username 대신 email 사용
            "user_id": user.id,
            "role": user.role.value
        }
    )
    
    return Token(access_token=access_token, token_type="bearer")
