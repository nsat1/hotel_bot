from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from config_data.config import settings

ASYNC_URI = settings.SQLALCHEMY_DATABASE_URI.replace("postgresql", "postgresql+asyncpg")

engine = create_async_engine(ASYNC_URI, pool_pre_ping=True, max_overflow=1)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
