from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from database.models import Base

from config.config import DB_URL

engine = create_async_engine(DB_URL, echo=False)

session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)