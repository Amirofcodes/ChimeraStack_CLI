import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from app.main import app

@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///./test.db", echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def override_get_db(test_db):
    async def _get_test_db():
        async with test_db() as session:
            yield session
    app.dependency_overrides[get_db] = _get_test_db
    return _get_test_db