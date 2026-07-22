import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from database import Base, engine

@pytest_asyncio.fixture(scope="module", autouse=True)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/")
    assert res.status_code == 200
    assert res.json()["message"] == "API running"

async def test_create_course_valid():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/courses/", json={"name": "Data Structures", "code": "CS101", "credits": 4})
    assert res.status_code == 201
    data = res.json()
    assert data["code"] == "CS101"
    assert data["id"] is not None

async def test_create_course_invalid_422():
    """Pydantic auto-returns 422 when required fields are missing."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/courses/", json={"name": "Missing Code"})
    assert res.status_code == 422

async def test_get_course_by_id():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/courses/", json={"name": "Algorithms", "code": "CS102", "credits": 4})
        course_id = create_res.json()["id"]
        res = await client.get(f"/api/courses/{course_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Algorithms"

async def test_get_course_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/courses/9999")
    assert res.status_code == 404

async def test_get_courses_pagination():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/courses/?skip=0&limit=1")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) <= 1
