from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: Optional[int] = None

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department_id: Optional[int] = None
    enrollment_year: int

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: Optional[int] = None
    enrollment_year: int
    model_config = ConfigDict(from_attributes=True)

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    grade: Optional[str] = None

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    grade: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_of_dept: str
    budget: float
    courses: List[CourseResponse] = []
    model_config = ConfigDict(from_attributes=True)
