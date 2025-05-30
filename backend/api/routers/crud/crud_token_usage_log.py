from sqlalchemy.ext.asyncio import AsyncSession
from db.models.token_usage_log import TokenUsageLog
from schemas.token_usage_log import TokenUsageLogCreate

async def create_token_usage_log(db: AsyncSession, user_id: int, ai_model_name: str, input_tokens: int, output_tokens: int):
    log = TokenUsageLog(
        user_id=user_id,
        ai_model_name=ai_model_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log
