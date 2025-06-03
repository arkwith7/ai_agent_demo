from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings
import aiosqlite

# SQLite URL을 수정하여 aiosqlite 드라이버를 명시적으로 지정
DATABASE_URL = settings.DATABASE_URL.replace('sqlite:///', 'sqlite+aiosqlite:///')

async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
