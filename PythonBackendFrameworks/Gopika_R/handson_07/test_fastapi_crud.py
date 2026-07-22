import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from database import Base, engine

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        res = await c.get("/")
    assert res.status_code == 200

async def test_create_and_get_course():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/courses/", json={"name": "Data Structures", "code": "CS101", "credits": 4})
        assert r.status_code == 201
        course_id = r.json()["id"]

        r = await c.get(f"/api/courses/{course_id}")
        assert r.status_code == 200
        assert r.json()["name"] == "Data Structures"

async def test_update_course():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/courses/", json={"name": "Algorithms", "code": "CS102", "credits": 3})
        course_id = r.json()["id"]

        r = await c.put(f"/api/courses/{course_id}", json={"credits": 4})
        assert r.status_code == 200
        assert r.json()["credits"] == 4

async def test_delete_course_204():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/courses/", json={"name": "To Delete", "code": "CS999", "credits": 1})
        course_id = r.json()["id"]

        r = await c.delete(f"/api/courses/{course_id}")
        assert r.status_code == 204  # No Content

        r = await c.get(f"/api/courses/{course_id}")
        assert r.status_code == 404  # Deleted

async def test_create_student_and_enrollment_with_background_task():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        # Create course
        course_r = await c.post("/api/courses/", json={"name": "OS", "code": "CS200", "credits": 4})
        course_id = course_r.json()["id"]

        # Create student
        student_r = await c.post("/api/students/", json={
            "first_name": "Alice", "last_name": "Smith",
            "email": "alice@test.com", "enrollment_year": 2024
        })
        assert student_r.status_code == 201
        student_id = student_r.json()["id"]

        # Enroll (triggers background email task)
        enroll_r = await c.post("/api/enrollments/", json={"student_id": student_id, "course_id": course_id})
        assert enroll_r.status_code == 201
        assert enroll_r.json()["student_id"] == student_id

async def test_course_students_join_query():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        res = await c.get("/api/courses/")
        courses = res.json()
        if courses:
            course_id = courses[0]["id"]
            res = await c.get(f"/api/courses/{course_id}/students/")
            assert res.status_code == 200
            assert isinstance(res.json(), list)

async def test_student_not_found_404():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        res = await c.get("/api/students/9999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Student not found"
