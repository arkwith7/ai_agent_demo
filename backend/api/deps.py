from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from core.security import decode_token
from db.session import get_db
from api.routers.crud import crud_user
from schemas.user import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_active_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UserRead:
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
    if user is None or not user.is_active:
        raise credentials_exception
    return UserRead.from_orm(user)
