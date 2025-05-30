from sqlalchemy.ext.asyncio import AsyncSession
from db.models.query_history import QueryHistory
from schemas.query_history import QueryHistoryCreate

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
