from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from db.session import get_db
from db.models.user import User, UserRole
from schemas.user import UserRead, UserCreate, UserUpdate, UserList, UserReadWithStats
from api.routers.crud import crud_user
from api.deps import get_current_admin_user, get_current_active_user, check_admin_or_self_access

router = APIRouter()

@router.get("/users", response_model=UserList, summary="사용자 목록 조회 (관리자 전용)")
async def get_users(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    role: Optional[UserRole] = Query(None, description="역할별 필터링"),
    active_only: bool = Query(True, description="활성 사용자만 조회"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    관리자만 접근 가능한 전체 사용자 목록 조회
    """
    skip = (page - 1) * size
    users, total = await crud_user.get_users(
        db=db, 
        skip=skip, 
        limit=size, 
        role_filter=role,
        active_only=active_only
    )
    
    return UserList(
        users=[UserRead.model_validate(user) for user in users],
        total=total,
        page=page,
        size=size
    )

@router.post("/users", response_model=UserRead, summary="새 사용자 생성 (관리자 전용)")
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    관리자가 새로운 사용자를 생성
    """
    # 사용자명 중복 확인
    if await crud_user.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # 이메일 중복 확인
    if await crud_user.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = await crud_user.create_user(db=db, user=user)
    return UserRead.model_validate(db_user)

@router.get("/users/{user_id}", response_model=UserReadWithStats, summary="사용자 상세 정보 조회")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(check_admin_or_self_access)
):
    """
    특정 사용자의 상세 정보 조회 (관리자 또는 본인만 가능)
    토큰 사용량 및 쿼리 히스토리 포함
    """
    user = await crud_user.get_user_with_stats(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserReadWithStats.model_validate(user)

@router.put("/users/{user_id}", response_model=UserRead, summary="사용자 정보 수정")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(check_admin_or_self_access)
):
    """
    사용자 정보 수정 (관리자 또는 본인만 가능)
    일반 사용자는 role 변경 불가
    """
    # 일반 사용자가 role을 변경하려는 경우 차단
    if (current_user.role != UserRole.ADMIN and 
        current_user.id == user_id and 
        user_update.role is not None):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot change your own role"
        )
    
    # 사용자명/이메일 중복 확인
    if user_update.username:
        existing_user = await crud_user.get_user_by_username(db, username=user_update.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    if user_update.email:
        existing_user = await crud_user.get_user_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
    
    updated_user = await crud_user.update_user(db, user_id=user_id, user_update=user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserRead.model_validate(updated_user)

@router.delete("/users/{user_id}", summary="사용자 삭제 (비활성화)")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    관리자만 사용자를 삭제(비활성화) 가능
    """
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    deleted_user = await crud_user.delete_user(db, user_id=user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deactivated successfully"}

@router.get("/users/{user_id}/token-usage", summary="사용자 토큰 사용량 통계")
async def get_user_token_usage(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(check_admin_or_self_access)
):
    """
    특정 사용자의 토큰 사용량 통계 조회 (관리자 또는 본인만 가능)
    """
    user = await crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    stats = await crud_user.get_user_token_usage_stats(db, user_id=user_id)
    
    return {
        "user_id": user_id,
        "username": user.username,
        "token_usage_by_model": stats
    }

@router.get("/me", response_model=UserReadWithStats, summary="내 정보 조회")
async def get_my_info(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    현재 로그인한 사용자의 정보 조회 (토큰 사용량 및 쿼리 히스토리 포함)
    """
    user = await crud_user.get_user_with_stats(db, user_id=current_user.id)
    return UserReadWithStats.model_validate(user)

@router.put("/me", response_model=UserRead, summary="내 정보 수정")
async def update_my_info(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    현재 로그인한 사용자의 정보 수정 (role 변경 불가)
    """
    # role 변경 시도 차단
    if user_update.role is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot change your own role"
        )
    
    # 사용자명/이메일 중복 확인
    if user_update.username:
        existing_user = await crud_user.get_user_by_username(db, username=user_update.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    if user_update.email:
        existing_user = await crud_user.get_user_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
    
    updated_user = await crud_user.update_user(db, user_id=current_user.id, user_update=user_update)
    return UserRead.model_validate(updated_user)
