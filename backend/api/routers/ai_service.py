from fastapi import APIRouter, Depends
from schemas.user import UserRead
from api import deps
from services import azure_openai_service
from api.routers.crud import crud_token_usage_log, crud_query_history
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks
from core.config import settings

router = APIRouter()

@router.post("/chat")
async def chat_with_ai(
    query: str,
    background_tasks: BackgroundTasks,
    current_user: UserRead = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    ai_response, input_tokens, output_tokens = await azure_openai_service.get_ai_response(query)
    background_tasks.add_task(
        crud_query_history.create_query_log,
        db=db,
        user_id=current_user.id,
        query_text=query,
        response_text=ai_response,
        ai_model_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
    )
    background_tasks.add_task(
        crud_token_usage_log.create_token_usage_log,
        db=db,
        user_id=current_user.id,
        ai_model_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )
    return {"response": ai_response}
