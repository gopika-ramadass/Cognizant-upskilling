"""
Pytest Suite for Hands-On 9: Authentication & Security
Verifies password hashing, duplicate registration 409 conflict,
JWT token generation, protected route 401 handling, and CORS response headers.
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from security import verify_password
from models import User

TEST_DB_FILE = os.path.join(os.path.dirname(__file__), "test_auth.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists(TEST_DB_FILE):
        try:
            os.remove(TEST_DB_FILE)
        except OSError:
            pass


# ---------------------------------------------------------------------------------
# Task 1 Tests: Password Hashing & Registration
# ---------------------------------------------------------------------------------
def test_user_registration_stores_only_hashed_password():
    """Step 90: Verify registration stores only bcrypt hash, never plain text."""
    payload = {"email": "student1@example.com", "password": "SecretPassword123"}
    response = client.post("/api/v1/auth/register/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "student1@example.com"
    assert "password" not in data  # Plain text never in response

    # Inspect database directly
    db = TestingSessionLocal()
    user_in_db = db.query(User).filter(User.email == "student1@example.com").first()
    db.close()

    assert user_in_db is not None
    assert user_in_db.hashed_password != "SecretPassword123"  # Not plain text
    assert user_in_db.hashed_password.startswith("$2b$")  # bcrypt prefix
    assert verify_password("SecretPassword123", user_in_db.hashed_password) is True


def test_duplicate_registration_returns_409_conflict():
    """Step 90: Verify second registration with same email returns 409 Conflict."""
    payload = {"email": "duplicate@example.com", "password": "Password123"}
    response1 = client.post("/api/v1/auth/register/", json=payload)
    assert response1.status_code == 201

    # Second registration attempt
    response2 = client.post("/api/v1/auth/register/", json=payload)
    assert response2.status_code == 409
    assert response2.json()["detail"] == "Email already registered"


# ---------------------------------------------------------------------------------
# Task 2 Tests: JWT Login, Protected Routes & CORS
# ---------------------------------------------------------------------------------
def test_jwt_login_success_and_failure():
    """Step 91: Verify login issues valid JWT token for correct credentials."""
    # 1. Register user
    reg_payload = {"email": "loginuser@example.com", "password": "CorrectPassword"}
    client.post("/api/v1/auth/register/", json=reg_payload)

    # 2. Login with correct password
    login_response = client.post(
        "/api/v1/auth/login/",
        data={"username": "loginuser@example.com", "password": "CorrectPassword"}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # 3. Login with wrong password
    wrong_login = client.post(
        "/api/v1/auth/login/",
        data={"username": "loginuser@example.com", "password": "WrongPassword"}
    )
    assert wrong_login.status_code == 401


def test_unauthenticated_and_protected_course_routes():
    """Step 93: Verify GET is unauthenticated while POST/DELETE return 401 without token."""
    # 1. GET courses (Public - 200 OK)
    get_res = client.get("/api/v1/courses/")
    assert get_res.status_code == 200
    assert get_res.json() == []

    # 2. POST course without auth token (401 Unauthorized)
    course_payload = {
        "title": "Web Security Principles",
        "code": "CS401",
        "department": "Computer Science",
        "credits": 4
    }
    post_unauth = client.post("/api/v1/courses/", json=course_payload)
    assert post_unauth.status_code == 401

    # 3. DELETE course without auth token (401 Unauthorized)
    del_unauth = client.delete("/api/v1/courses/1/")
    assert del_unauth.status_code == 401

    # 4. Register & Login to get token
    client.post("/api/v1/auth/register/", json={"email": "teacher@example.com", "password": "TeacherPassword"})
    login_res = client.post(
        "/api/v1/auth/login/",
        data={"username": "teacher@example.com", "password": "TeacherPassword"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 5. POST course with valid token (201 Created)
    post_auth = client.post("/api/v1/courses/", json=course_payload, headers=headers)
    assert post_auth.status_code == 201
    course_id = post_auth.json()["id"]

    # 6. DELETE course with valid token (200 OK)
    del_auth = client.delete(f"/api/v1/courses/{course_id}/", headers=headers)
    assert del_auth.status_code == 200


def test_cors_headers_configuration():
    """Step 94: Verify CORS allows localhost:3000."""
    headers = {"Origin": "http://localhost:3000"}
    response = client.options("/api/v1/courses/", headers=headers)
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
