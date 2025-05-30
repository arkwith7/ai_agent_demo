from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import func, desc
from typing import Optional, List
from db.models.user import User, UserRole
from db.models.token_usage_log import TokenUsageLog
from db.models.query_history import QueryHistory
from schemas.user import UserCreate, UserUpdate
from core.security import get_password_hash

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def get_user_with_stats(db: AsyncSession, user_id: int):
    """사용자 정보와 토큰 사용량, 쿼리 히스토리를 함께 조회"""
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.token_usage_logs),
            selectinload(User.query_histories)
        )
        .where(User.id == user_id)
    )
    user = result.scalars().first()
    
    if user:
        # 토큰 사용량 통계 계산
        total_input_tokens = sum(log.input_tokens for log in user.token_usage_logs)
        total_output_tokens = sum(log.output_tokens for log in user.token_usage_logs)
        total_queries = len(user.query_histories)
        
        # 사용자 객체에 통계 정보 추가
        user.total_input_tokens = total_input_tokens
        user.total_output_tokens = total_output_tokens
        user.total_queries = total_queries
    
    return user

async def get_users(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    role_filter: Optional[UserRole] = None,
    active_only: bool = True
) -> tuple[List[User], int]:
    """사용자 목록 조회 (페이징 및 필터링 지원)"""
    query = select(User)
    
    # 필터링 조건 추가
    if role_filter:
        query = query.where(User.role == role_filter)
    if active_only:
        query = query.where(User.is_active == True)
    
    # 전체 개수 조회
    count_query = select(func.count(User.id))
    if role_filter:
        count_query = count_query.where(User.role == role_filter)
    if active_only:
        count_query = count_query.where(User.is_active == True)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 페이징된 결과 조회
    query = query.order_by(desc(User.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return users, total

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    """사용자 정보 업데이트"""
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        return None
    
    # 업데이트할 필드들 설정
    update_data = user_update.model_dump(exclude_unset=True)
    
    # 비밀번호가 포함된 경우 해시화
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    """사용자 삭제 (실제로는 비활성화)"""
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        return None
    
    db_user.is_active = False
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_token_usage_stats(db: AsyncSession, user_id: int):
    """사용자별 토큰 사용량 통계"""
    result = await db.execute(
        select(
            func.sum(TokenUsageLog.input_tokens).label('total_input'),
            func.sum(TokenUsageLog.output_tokens).label('total_output'),
            func.count(TokenUsageLog.id).label('total_requests'),
            TokenUsageLog.ai_model_name
        )
        .where(TokenUsageLog.user_id == user_id)
        .group_by(TokenUsageLog.ai_model_name)
    )
    
    return [
        {
            "model": row.ai_model_name,
            "total_input_tokens": row.total_input or 0,
            "total_output_tokens": row.total_output or 0,
            "total_requests": row.total_requests or 0,
        }
        for row in result
    ]
