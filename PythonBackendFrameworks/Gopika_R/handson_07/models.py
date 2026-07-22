from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    head_of_dept = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    courses = relationship('Course', back_populates='department', cascade='all, delete-orphan')
    students = relationship('Student', back_populates='department', cascade='all, delete-orphan')


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    department = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    enrollment_year = Column(Integer, nullable=False)
    department = relationship('Department', back_populates='students')
    enrollments = relationship('Enrollment', back_populates='student', cascade='all, delete-orphan')


class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    grade = Column(String(5), nullable=True)
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')
