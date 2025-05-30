from pydantic import BaseModel
from datetime import datetime

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
