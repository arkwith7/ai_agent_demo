from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime
from db.session import get_db
from db.models.user import User, UserRole
from schemas.user import UserRead, UserCreate, UserUpdate, UserList, UserReadWithStats
from schemas.query_history import ChatHistoryList, QueryHistoryRead, ChatHistorySummary
from api.routers.crud import crud_user, crud_query_history, crud_token_usage_log
from api.deps import get_current_admin_user, get_current_active_user, check_admin_or_self_access
from services import azure_openai_service
from core.config import settings

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

# ==================== 채팅 히스토리 관리 API ====================

@router.get("/me/chat-history", response_model=ChatHistoryList, summary="내 채팅 히스토리 조회")
async def get_my_chat_history(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    현재 로그인한 사용자의 채팅 히스토리 조회 (페이징 지원)
    """
    skip = (page - 1) * size
    histories, total = await crud_query_history.get_user_chat_history(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=size
    )
    
    return ChatHistoryList(
        histories=[QueryHistoryRead.model_validate(history) for history in histories],
        total=total,
        page=page,
        size=size
    )

@router.get("/me/chat-history/search", response_model=ChatHistoryList, summary="채팅 히스토리 검색")
async def search_my_chat_history(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    keyword: Optional[str] = Query(None, description="검색 키워드 (질문 또는 답변에서 검색)"),
    start_date: Optional[datetime] = Query(None, description="시작 날짜 (YYYY-MM-DD 형식)"),
    end_date: Optional[datetime] = Query(None, description="종료 날짜 (YYYY-MM-DD 형식)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    채팅 히스토리 검색 및 필터링
    - 키워드로 질문/답변 내용 검색
    - 날짜 범위 필터링
    """
    skip = (page - 1) * size
    histories, total = await crud_query_history.get_user_chat_history(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=size,
        keyword=keyword,
        start_date=start_date,
        end_date=end_date
    )
    
    return ChatHistoryList(
        histories=[QueryHistoryRead.model_validate(history) for history in histories],
        total=total,
        page=page,
        size=size
    )

@router.post("/me/chat-history/{history_id}/summarize", response_model=ChatHistorySummary, summary="대화 요약")
async def summarize_chat_history(
    history_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    특정 채팅 히스토리의 대화 내용을 AI로 요약
    """
    # 해당 히스토리가 현재 사용자 소유인지 확인
    history = await crud_query_history.get_chat_history_by_id(
        db=db, 
        history_id=history_id, 
        user_id=current_user.id
    )
    
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat history not found"
        )
    
    try:
        # AI 요약 생성
        summary, input_tokens, output_tokens = await azure_openai_service.summarize_conversation(
            query_text=history.query_text,
            response_text=history.response_text
        )
        
        # 토큰 사용량 로그 (백그라운드 작업)
        if input_tokens > 0 and output_tokens > 0:
            background_tasks.add_task(
                crud_token_usage_log.create_token_usage_log,
                db=db,
                user_id=current_user.id,
                ai_model_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
        
        return ChatHistorySummary(
            history_id=history.id,
            original_query=history.query_text,
            original_response=history.response_text,
            summary=summary,
            created_at=history.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate summary: {str(e)}"
        )

# ==================== 관리자용 채팅 히스토리 API ====================

@router.get("/users/{user_id}/chat-history", response_model=ChatHistoryList, summary="사용자 채팅 히스토리 조회 (관리자)")
async def get_user_chat_history_admin(
    user_id: int,
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    keyword: Optional[str] = Query(None, description="검색 키워드"),
    start_date: Optional[datetime] = Query(None, description="시작 날짜"),
    end_date: Optional[datetime] = Query(None, description="종료 날짜"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    관리자가 특정 사용자의 채팅 히스토리 조회
    """
    # 사용자 존재 확인
    user = await crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    skip = (page - 1) * size
    histories, total = await crud_query_history.get_user_chat_history(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=size,
        keyword=keyword,
        start_date=start_date,
        end_date=end_date
    )
    
    return ChatHistoryList(
        histories=[QueryHistoryRead.model_validate(history) for history in histories],
        total=total,
        page=page,
        size=size
    )
