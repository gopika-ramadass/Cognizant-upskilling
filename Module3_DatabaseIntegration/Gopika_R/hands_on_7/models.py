"""
================================================================================
DIGITAL NURTURE 5.0 | MODULE 3: DATABASE INTEGRATION
HANDS-ON 7: Task 1 - SQLAlchemy Models & Engine Connection
================================================================================
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(100), nullable=False)
    head_of_dept = Column(String(100))
    budget = Column(Numeric(12, 2))
    
    # Relationships
    students = relationship('Student', back_populates='department')
    courses = relationship('Course', back_populates='department')
    professors = relationship('Professor', back_populates='department')


class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(Date)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    enrollment_year = Column(Integer)
    
    # Relationships
    department = relationship('Department', back_populates='students')
    enrollments = relationship('Enrollment', back_populates='student')


class Course(Base):
    __tablename__ = 'courses'
    
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(150), nullable=False)
    course_code = Column(String(20), unique=True)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    
    # Relationships
    department = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')


class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    enrollment_date = Column(Date)
    grade = Column(String(2), nullable=True)
    
    # Relationships
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')


class Professor(Base):
    __tablename__ = 'professors'
    
    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    prof_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    salary = Column(Numeric(10, 2))
    
    # Relationships
    department = relationship('Department', back_populates='professors')


# Database Connection Setup
DATABASE_URL = "sqlite:///college_db_orm.db"
engine = create_engine(DATABASE_URL, echo=True)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
