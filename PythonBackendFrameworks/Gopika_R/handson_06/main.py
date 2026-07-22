from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from contextlib import asynccontextmanager

from database import engine, Base, get_db
from models import Course, Department
from schemas import CourseCreate, CourseUpdate, CourseResponse, DepartmentResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title='Course Management API',
    version='1.0',
    lifespan=lifespan
)

@app.get('/')
async def root():
    """
    Root endpoint returning basic API status message.
    """
    return {'message': 'API running'}


@app.post('/api/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    """
    POST /api/courses/
    FastAPI validates request body against Pydantic schema CourseCreate (returns 422 automatically if invalid).
    Inserts course into SQLite via async SQLAlchemy.
    """
    db_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id
    )
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    """
    GET /api/courses/{course_id}
    Path parameter course_id is automatically validated as integer by FastAPI.
    """
    result = await db.execute(select(Course).filter(Course.id == course_id))
    db_course = result.scalars().first()
    if not db_course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} not found")
    return db_course


@app.get('/api/courses/', response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    GET /api/courses/
    Query parameters: skip (default 0), limit (default 10), department_id (optional).
    Implements pagination and filtering using async ORM queries.
    """
    query = select(Course)
    if department_id is not None:
        query = query.filter(Course.department_id == department_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
