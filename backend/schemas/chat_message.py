from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any

class ChatMessageBase(BaseModel):
    sender: str  # 'user' or 'agent'
    content: str
    content_type: str = "text"  # 'text', 'table', 'chart', etc.
    structured_data: Optional[Any] = None

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageRead(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionBase(BaseModel):
    pass

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionRead(ChatSessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageRead] = []

    class Config:
        from_attributes = True
