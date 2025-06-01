from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from db.models.chat_message import ChatSession, ChatMessage
from typing import Optional, List
from datetime import datetime

async def create_chat_session(db: AsyncSession, user_id: int) -> ChatSession:
    session = ChatSession(user_id=user_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

async def add_message_to_session(db: AsyncSession, session_id: int, sender: str, content: str, content_type: str = "text", structured_data=None) -> ChatMessage:
    message = ChatMessage(
        session_id=session_id,
        sender=sender,
        content=content,
        content_type=content_type,
        structured_data=structured_data
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message

async def get_user_sessions(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 20) -> List[ChatSession]:
    query = select(ChatSession).where(ChatSession.user_id == user_id).order_by(desc(ChatSession.updated_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_session_messages(db: AsyncSession, session_id: int) -> List[ChatMessage]:
    query = select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at)
    result = await db.execute(query)
    return result.scalars().all()
