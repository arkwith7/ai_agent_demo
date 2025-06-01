from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api import deps
from db.session import get_db
from schemas.chat_message import ChatSessionRead, ChatMessageRead, ChatMessageCreate
from api.routers.crud import crud_chat_message
from typing import List

router = APIRouter()

@router.post("/sessions", response_model=ChatSessionRead)
async def create_session(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(deps.get_current_active_user)
):
    session = await crud_chat_message.create_chat_session(db, current_user.id)
    return ChatSessionRead.from_orm(session)

@router.get("/sessions", response_model=List[ChatSessionRead])
async def list_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(deps.get_current_active_user)
):
    sessions = await crud_chat_message.get_user_sessions(db, current_user.id, skip, limit)
    return [ChatSessionRead.from_orm(s) for s in sessions]

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageRead])
async def get_session_messages(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(deps.get_current_active_user)
):
    # TODO: session ownership check
    messages = await crud_chat_message.get_session_messages(db, session_id)
    return [ChatMessageRead.from_orm(m) for m in messages]

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageRead)
async def add_message(
    session_id: int,
    message: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(deps.get_current_active_user)
):
    # TODO: session ownership check
    msg = await crud_chat_message.add_message_to_session(
        db, session_id, message.sender, message.content, message.content_type, message.structured_data
    )
    return ChatMessageRead.from_orm(msg)
