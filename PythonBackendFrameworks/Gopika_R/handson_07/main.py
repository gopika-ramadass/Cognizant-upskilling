import logging
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import engine, Base, get_db
from models import Course, Student, Enrollment
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title='Course Management API',
    description='A complete RESTful API for managing courses, students and enrollments using FastAPI with async SQLAlchemy.',
    version='2.0',
    contact={'name': 'Gopika R', 'email': 'gopika200538@gmail.com'},
    license_info={'name': 'MIT'},
    lifespan=lifespan
)

# ─── Background Task ─────────────────────────────────────────────────────────

def send_confirmation_email(student_email: str, course_name: str):
    """
    BackgroundTask: Runs asynchronously after sending enrollment HTTP response.
    Simulates sending a confirmation email after enrollment.
    """
    logger.info(f"[BACKGROUND] Sending enrollment confirmation to {student_email} for course '{course_name}'")


# ─── Root ─────────────────────────────────────────────────────────────────────

@app.get('/', tags=['Health'], summary='API Health Check', response_description='API status message')
async def root():
    return {'message': 'Course Management API v2.0 running'}


# ─── Courses ──────────────────────────────────────────────────────────────────

@app.get('/api/courses/', response_model=List[CourseResponse], tags=['Courses'],
         summary='List all courses', response_description='List of course objects')
async def get_courses(skip: int = 0, limit: int = 10, department_id: Optional[int] = None,
                      db: AsyncSession = Depends(get_db)):
    query = select(Course)
    if department_id is not None:
        query = query.filter(Course.department_id == department_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@app.post('/api/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED,
          tags=['Courses'], summary='Create a new course')
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'],
         summary='Get a course by ID')
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.put('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'],
         summary='Update a course by ID')
async def update_course(course_id: int, course_data: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    for key, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'],
            summary='Delete a course by ID')
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(course)
    await db.commit()


@app.get('/api/courses/{course_id}/students/', response_model=List[StudentResponse], tags=['Courses'],
         summary='Get all students enrolled in a course')
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    student_result = await db.execute(
        select(Student).join(Enrollment).filter(Enrollment.course_id == course_id)
    )
    return student_result.scalars().all()


# ─── Students ─────────────────────────────────────────────────────────────────

@app.get('/api/students/', response_model=List[StudentResponse], tags=['Students'])
async def get_students(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).offset(skip).limit(limit))
    return result.scalars().all()


@app.post('/api/students/', response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=['Students'])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


@app.get('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    return student


@app.delete('/api/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    await db.delete(student)
    await db.commit()


# ─── Enrollments (with BackgroundTask) ────────────────────────────────────────

@app.post('/api/enrollments/', response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED,
          tags=['Enrollments'], summary='Enroll a student in a course (sends background confirmation email)')
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # Validate student and course exist
    student_result = await db.execute(select(Student).filter(Student.id == enrollment.student_id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    course_result = await db.execute(select(Course).filter(Course.id == enrollment.course_id))
    course = course_result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')

    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)

    # Background task: runs after HTTP response is sent
    background_tasks.add_task(send_confirmation_email, student.email, course.name)

    return db_enrollment
