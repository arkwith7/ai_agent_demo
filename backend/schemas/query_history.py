from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class QueryHistoryCreate(BaseModel):
    query_text: str
    response_text: str
    ai_model_name: str

class QueryHistoryRead(QueryHistoryCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatHistoryList(BaseModel):
    """채팅 히스토리 목록 응답"""
    histories: List[QueryHistoryRead]
    total: int
    page: int
    size: int

class ChatHistorySummary(BaseModel):
    """대화 요약 응답"""
    history_id: int
    original_query: str
    original_response: str
    summary: str
    created_at: datetime
