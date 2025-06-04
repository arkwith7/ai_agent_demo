from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from core.agent import StockAnalysisAgent, get_agent
from schemas.analysis import AnalysisRequest, AnalysisResponse
from schemas.user import User
from schemas.chat import MessageType
from api.deps import get_current_active_user

router = APIRouter()

@router.post("/message", response_model=AnalysisResponse)
async def send_message(
    request: AnalysisRequest,
    agent: StockAnalysisAgent = Depends(get_agent),
    current_user: User = Depends(get_current_active_user)
):
    """채팅 메시지를 처리합니다."""
    response = await agent.process_chat_message(request, current_user)
    if response.message_type == MessageType.ERROR:
        raise HTTPException(status_code=500, detail=response.content)
    return response

@router.get("/history", response_model=List[AnalysisResponse])
async def get_chat_history(
    page: int = 1,
    size: int = 20,
    agent: StockAnalysisAgent = Depends(get_agent),
    current_user: User = Depends(get_current_active_user)
):
    """채팅 기록을 반환합니다."""
    history = await agent.get_chat_history(user_id=current_user.id, page=page, size=size)
    return history

@router.get("/history/search", response_model=List[AnalysisResponse])
async def search_chat_history(
    keyword: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    agent: StockAnalysisAgent = Depends(get_agent),
    current_user: User = Depends(get_current_active_user)
):
    """채팅 기록을 검색합니다."""
    results = await agent.search_chat_history(
        user_id=current_user.id, 
        keyword=keyword, 
        start_date=start_date, 
        end_date=end_date, 
        page=page, 
        size=size
    )
    return results

@router.post("/history/{history_id}/summarize", response_model=AnalysisResponse)
async def summarize_chat_history(
    history_id: int,
    agent: StockAnalysisAgent = Depends(get_agent),
    current_user: User = Depends(get_current_active_user)
):
    """특정 채팅 기록을 요약합니다."""
    summary_response = await agent.summarize_chat_history(history_id=history_id, user_id=current_user.id)
    if summary_response.message_type == MessageType.ERROR:
        raise HTTPException(status_code=404, detail=summary_response.content)
    return summary_response 