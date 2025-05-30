from pydantic import BaseModel
from datetime import datetime

class TokenUsageLogCreate(BaseModel):
    ai_model_name: str
    input_tokens: int
    output_tokens: int

class TokenUsageLogRead(TokenUsageLogCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
