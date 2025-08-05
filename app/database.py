from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True)


AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


Base = declarative_base()


async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection error: {str(e)}"
        )
