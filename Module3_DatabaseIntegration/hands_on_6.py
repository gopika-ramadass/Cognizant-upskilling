# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    
    department_id = Column(Integer, primary_key=True, autoincrement=True) [cite: 491]
    dept_name = Column(String(100), nullable=False) [cite: 491]
    head_of_dept = Column(String(100))  # Renamed as per Hands-On 1 [cite: 491, 684]
    budget = Column(Numeric(12, 2)) [cite: 491]
    
    # Relationships
    students = relationship('Student', back_populates='department')
    courses = relationship('Course', back_populates='department')
    professors = relationship('Professor', back_populates='department')

class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True, autoincrement=True) [cite: 489]
    first_name = Column(String(50), nullable=False) [cite: 489]
    last_name = Column(String(50), nullable=False) [cite: 489]
    email = Column(String(100), unique=True, nullable=False) [cite: 489]
    date_of_birth = Column(Date) [cite: 489]
    department_id = Column(Integer, ForeignKey('departments.department_id')) [cite: 489]
    enrollment_year = Column(Integer) [cite: 489]
    
    # Relationships
    department = relationship('Department', back_populates='students') [cite: 864]
    enrollments = relationship('Enrollment', back_populates='student')

class Course(Base):
    __tablename__ = 'courses'
    
    course_id = Column(Integer, primary_key=True, autoincrement=True) [cite: 493]
    course_name = Column(String(150), nullable=False) [cite: 493]
    course_code = Column(String(20), unique=True) [cite: 493]
    credits = Column(Integer) [cite: 493]
    department_id = Column(Integer, ForeignKey('departments.department_id')) [cite: 493]
    
    # Relationships
    department = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')

class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True) [cite: 495]
    student_id = Column(Integer, ForeignKey('students.student_id')) [cite: 495]
    course_id = Column(Integer, ForeignKey('courses.course_id')) [cite: 498]
    enrollment_date = Column(Date) [cite: 498]
    grade = Column(String(2), nullable=True) [cite: 498]
    
    # Relationships
    student = relationship('Student', back_populates='enrollments') [cite: 865]
    course = relationship('Course', back_populates='enrollments') [cite: 865]

class Professor(Base):
    __tablename__ = 'professors'
    
    professor_id = Column(Integer, primary_key=True, autoincrement=True) [cite: 500]
    prof_name = Column(String(100), nullable=False) [cite: 500]
    email = Column(String(100), unique=True) [cite: 500]
    department_id = Column(Integer, ForeignKey('departments.department_id')) [cite: 500]
    salary = Column(Numeric(10, 2)) [cite: 500]
    
    # Relationships
    department = relationship('Department', back_populates='professors')

# Database connection details (Adjust string for PostgreSQL or MySQL as needed)
DATABASE_URL = "postgresql://username:password@localhost:5432/college_db_orm" [cite: 862, 866]
engine = create_engine(DATABASE_URL, echo=False) # Echo will be toggled dynamically in crud.py [cite: 862, 875]

if __name__ == "__main__":
    # Auto-creates tables in the fresh database [cite: 866]
    Base.metadata.create_all(engine) [cite: 866]
    print("Database tables created successfully!") [cite: 868]