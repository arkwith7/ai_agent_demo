from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from core.security import decode_token
from db.session import get_db
from api.routers.crud import crud_user
from schemas.user import UserRead
from db.models.user import UserRole, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """현재 인증된 사용자 정보 반환"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = await crud_user.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """현재 활성화된 사용자 정보 반환"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """관리자 권한 확인 후 사용자 정보 반환"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin access required."
        )
    return current_user

def require_admin_or_self(target_user_id: int):
    """관리자이거나 본인인 경우에만 접근 허용하는 의존성"""
    def check_permission(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        if current_user.role != UserRole.ADMIN and current_user.id != target_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions. Admin access or self access required."
            )
        return current_user
    return check_permission

async def check_admin_or_self_access(
    user_id: int,
    current_user: User = Depends(get_current_active_user)
) -> User:
    """관리자이거나 본인인 경우에만 접근 허용"""
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin access or self access required."
        )
    return current_user
