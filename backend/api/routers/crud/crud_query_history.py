from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, desc, or_
from db.models.query_history import QueryHistory
from schemas.query_history import QueryHistoryCreate
from typing import Optional, List, Tuple
from datetime import datetime

async def create_query_log(db: AsyncSession, user_id: int, query_text: str, response_text: str, ai_model_name: str):
    log = QueryHistory(
        user_id=user_id,
        query_text=query_text,
        response_text=response_text,
        ai_model_name=ai_model_name
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

async def get_user_chat_history(
    db: AsyncSession, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 20,
    keyword: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Tuple[List[QueryHistory], int]:
    """사용자의 채팅 히스토리 조회 (페이징, 검색, 필터링 지원)"""
    
    # 기본 쿼리
    query = select(QueryHistory).where(QueryHistory.user_id == user_id)
    count_query = select(func.count(QueryHistory.id)).where(QueryHistory.user_id == user_id)
    
    # 키워드 검색
    if keyword:
        search_filter = or_(
            QueryHistory.query_text.ilike(f"%{keyword}%"),
            QueryHistory.response_text.ilike(f"%{keyword}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)
    
    # 날짜 범위 필터링
    if start_date:
        query = query.where(QueryHistory.created_at >= start_date)
        count_query = count_query.where(QueryHistory.created_at >= start_date)
    
    if end_date:
        query = query.where(QueryHistory.created_at <= end_date)
        count_query = count_query.where(QueryHistory.created_at <= end_date)
    
    # 전체 개수 조회
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 페이징된 결과 조회 (최신순 정렬)
    query = query.order_by(desc(QueryHistory.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    histories = result.scalars().all()
    
    return histories, total

async def get_chat_history_by_id(db: AsyncSession, history_id: int, user_id: int) -> Optional[QueryHistory]:
    """특정 채팅 히스토리 조회 (사용자 소유 확인)"""
    query = select(QueryHistory).where(
        QueryHistory.id == history_id,
        QueryHistory.user_id == user_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()
