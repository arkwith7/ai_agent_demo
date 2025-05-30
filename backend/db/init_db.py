import asyncio
from db.base_class import Base
from db.session import async_engine
import db.models.user  # noqa: F401
import db.models.token_usage_log  # noqa: F401
import db.models.query_history  # noqa: F401

async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All tables created.")

if __name__ == "__main__":
    asyncio.run(init_models())
