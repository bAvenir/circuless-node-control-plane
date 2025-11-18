from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from utils import config

settings = config.settings

# Async engine for FastAPI
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_LOG,  # Set to False in production
    future=True
)

AsyncSessionLocal = sessionmaker(
    engine, class_= AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Dependency for database sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
