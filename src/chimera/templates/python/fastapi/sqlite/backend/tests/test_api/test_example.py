import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.db.session import get_db

@pytest.mark.asyncio
async def test_create_example():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/examples/",
            params={"title": "Test", "description": "Test Description"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Test"

@pytest.mark.asyncio
async def test_read_examples():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/examples/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)