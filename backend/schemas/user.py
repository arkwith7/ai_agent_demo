from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from db.models.user import UserRole
from schemas.token_usage_log import TokenUsageLogRead
from schemas.query_history import QueryHistoryRead

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일")
    username: str = Field(..., description="사용자 이름")
    is_active: bool = Field(default=True, description="계정 활성화 상태")
    is_superuser: bool = Field(default=False, description="관리자 여부")

class UserCreate(UserBase):
    password: str = Field(..., description="비밀번호")
    role: Optional[UserRole] = UserRole.USER

class UserRead(UserBase):
    id: int
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
    email: Optional[EmailStr] = Field(default=None, description="사용자 이메일")
    username: Optional[str] = Field(default=None, description="사용자 이름")
    password: Optional[str] = Field(default=None, description="비밀번호")
    is_active: Optional[bool] = Field(default=None, description="계정 활성화 상태")
    role: Optional[UserRole] = None

class UserList(BaseModel):
    users: List[UserRead]
    total: int
    page: int
    size: int

class User(UserBase):
    id: int = Field(..., description="사용자 ID")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")
    updated_at: datetime = Field(default_factory=datetime.now, description="수정 시간")

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str = Field(..., description="해시된 비밀번호")
