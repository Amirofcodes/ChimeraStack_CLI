from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from .base import SessionLocal

async def get_db() -> Generator[AsyncSession, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()