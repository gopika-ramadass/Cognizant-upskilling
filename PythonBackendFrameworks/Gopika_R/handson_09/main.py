"""
Hands-On 9: Authentication & Security — JWT, OAuth2 & OWASP
FastAPI Application implementing secure password hashing, JWT authentication,
protected routes, and CORS configuration.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from database import engine, Base, get_db
from models import User, Course
from schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    Token,
    CourseCreate,
    CourseResponse,
)
from security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hands-On 9: Authentication & Security API",
    version="1.0.0",
    description="FastAPI service with JWT Authentication, bcrypt hashing, protected routes, and CORS."
)

# ---------------------------------------------------------------------------------
# Task 2 - Step 94: CORS Configuration
# ---------------------------------------------------------------------------------
# OWASP / CORS Explanation (Task 2 - Step 95):
# - CORS (Cross-Origin Resource Sharing) is a security mechanism enforced by browsers.
# - The server sends `Access-Control-Allow-Origin` headers specifying allowed client origins.
# - Note: CORS does NOT protect server-side APIs against direct curl or backend requests;
#   it prevents malicious browser web applications on other domains from reading response data.
# ---------------------------------------------------------------------------------
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------------
# Task 1 - Step 88: User Registration Endpoint
# ---------------------------------------------------------------------------------
@app.post(
    "/api/v1/auth/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user with bcrypt password hashing"
)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    User Registration Endpoint (Task 1 - Step 88):
    1. Validates email format via Pydantic validator.
    2. Checks if email is already registered; returns 409 Conflict if duplicate.
    3. Hashes password using bcrypt (get_password_hash).
    4. Saves user to database. Plain-text password is NEVER stored or logged (Step 89).
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash plain-text password using bcrypt before saving
    hashed_pwd = get_password_hash(user_in.password)
    
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_pwd,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ---------------------------------------------------------------------------------
# Task 2 - Step 91: JWT Login Endpoints
# ---------------------------------------------------------------------------------
# Explanation: OAuth2 Authorization Code Flow vs Simple JWT Login (Task 2 - Step 95)
# ---------------------------------------------------------------------------------
# 1. Simple JWT Login (Resource Owner Password Credentials):
#    - Client submits email & password directly to POST /api/v1/auth/login/.
#    - API verifies credentials and returns JWT token directly to client.
#    - Best for first-party, trusted user interfaces owned by the same organization.
#
# 2. OAuth2 Authorization Code Flow:
#    - User is redirected to an external Authorization Server (e.g. Google, GitHub, Okta).
#    - User authenticates on the authorization server's domain (app never sees password).
#    - Authorization server redirects back to client URI with a temporary Authorization Code.
#    - Client backend exchanges authorization code for access/refresh tokens.
#    - Ideal for third-party client integrations where passwords should never be shared.
# ---------------------------------------------------------------------------------
@app.post(
    "/api/v1/auth/login/",
    response_model=Token,
    summary="Login user and return JWT Bearer token (Form data)"
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    JWT Login Endpoint (Task 2 - Step 91):
    Accepts OAuth2 password form data (username & password), verifies using bcrypt,
    and returns a JWT token valid for 30 minutes.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post(
    "/api/v1/auth/login/json",
    response_model=Token,
    summary="Login user and return JWT Bearer token (JSON body)"
)
def login_json(
    json_login: LoginRequest,
    db: Session = Depends(get_db)
):
    """JSON variant of JWT login endpoint."""
    user = db.query(User).filter(User.email == json_login.email).first()
    if not user or not verify_password(json_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------------------------------------------------------------------
# Task 2 - Step 93: Unauthenticated & Protected Course Endpoints
# ---------------------------------------------------------------------------------
@app.get(
    "/api/v1/courses/",
    response_model=List[CourseResponse],
    summary="Get all courses (Public unauthenticated endpoint)"
)
def get_courses(db: Session = Depends(get_db)):
    """Unauthenticated endpoint: Anyone can view available courses (Task 2 - Step 93)."""
    return db.query(Course).all()


@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new course (Protected endpoint — Requires JWT token)"
)
def create_course(
    course_in: CourseCreate,
    current_user: User = Depends(get_current_user),  # Task 2 - Step 93
    db: Session = Depends(get_db)
):
    """Protected endpoint: Requires valid JWT token in Authorization header."""
    new_course = Course(
        title=course_in.title,
        code=course_in.code,
        department=course_in.department,
        credits=course_in.credits
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.delete(
    "/api/v1/courses/{course_id}/",
    status_code=status.HTTP_200_OK,
    summary="Delete a course (Protected endpoint — Requires JWT token)"
)
def delete_course(
    course_id: int,
    current_user: User = Depends(get_current_user),  # Task 2 - Step 93
    db: Session = Depends(get_db)
):
    """Protected endpoint: Requires valid JWT token in Authorization header."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found"
        )
    db.delete(course)
    db.commit()
    return {"detail": f"Course {course_id} deleted successfully"}


@app.get("/")
def root():
    return {
        "message": "Hands-On 9 API (JWT, OAuth2 & Security) Running",
        "docs": "/docs"
    }
