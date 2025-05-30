from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from db.models.user import UserRole
from schemas.token_usage_log import TokenUsageLogRead
from schemas.query_history import QueryHistoryRead

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.USER

class UserRead(UserBase):
    id: int
    is_active: bool
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

class UserReadWithStats(UserRead):
    token_usage_logs: List[TokenUsageLogRead] = []
    query_histories: List[QueryHistoryRead] = []
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_queries: int = 0

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

class UserList(BaseModel):
    users: List[UserRead]
    total: int
    page: int
    size: int
