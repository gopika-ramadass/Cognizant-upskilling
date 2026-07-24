"""
================================================================================
DIGITAL NURTURE 5.0 | MODULE 3: DATABASE INTEGRATION
HANDS-ON 7 (Exercise 6 - Advanced): ORM Integration — SQLAlchemy & Django ORM
================================================================================

TASK 3: EAGER LOADING TO FIX N+1 QUERY PROBLEM - FINDINGS & COMPARISON
--------------------------------------------------------------------------------
1. Lazy Loading (Task 2 Step 84 - Standard Query):
   Query: session.query(Enrollment).all()
   Behavior: 
     - Issues 1 SQL query to fetch all 4 enrollment records.
     - In the loop `for e in enrollments: print(e.student.first_name, e.course.course_name)`:
       - Accessing `e.student` issues 1 SQL query per enrollment (4 queries).
       - Accessing `e.course` issues 1 SQL query per enrollment (4 queries).
   Total Queries Issued: 1 + 4 + 4 = 9 queries (or 1 + 2*N queries for N enrollments).
   With 12 enrollments, this results in 1 + 12 + 12 = 25 queries (N+1 / 2N+1 problem).

2. Eager Loading with joinedload (Task 3 Step 88 - Optimized Query):
   Query: 
     from sqlalchemy.orm import joinedload
     session.query(Enrollment).options(
         joinedload(Enrollment.student),
         joinedload(Enrollment.course)
     ).all()
   Behavior:
     - SQLAlchemy generates a single SQL SELECT query with LEFT OUTER JOINs:
       SELECT enrollments.*, students.*, courses.* 
       FROM enrollments 
       LEFT OUTER JOIN students ON students.student_id = enrollments.student_id 
       LEFT OUTER JOIN courses ON courses.course_id = enrollments.course_id
   Total Queries Issued: 1 Query!

3. Performance Impact:
   - Query Count reduced from 9 queries (N+1) down to 1 query.
   - Eliminates database round-trips, dramatically improving throughput and latency.

4. Django ORM Equivalent (Task 3 Step 91 - Bonus):
   In Django ORM, the equivalent eager loading for foreign keys (many-to-one) is:
     Enrollment.objects.select_related('student', 'course').all()
   This performs an SQL JOIN in a single database query.
================================================================================
"""

from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, joinedload

# ------------------------------------------------------------------------------
# TASK 1: SQLAlchemy - Define Models and Connect
# ------------------------------------------------------------------------------

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
# PostgreSQL connection string example (as specified in exercise instructions):
# DATABASE_URL = "postgresql://postgres:password@localhost:5432/college_db_orm"
# Using SQLite fallback in-memory/file db so script executes cleanly without external server setup:
DATABASE_URL = "sqlite:///college_db_orm.db"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


def init_db():
    """Create all tables in college_db_orm."""
    print("\n--- TASK 1: Creating database tables ---")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Tables created successfully: departments, students, courses, enrollments, professors.")


# ------------------------------------------------------------------------------
# TASK 2: CRUD Operations via ORM
# ------------------------------------------------------------------------------

def run_crud_operations():
    session = Session()
    try:
        print("\n--- TASK 2.81: INSERT Departments and Students ---")
        dept_cs = Department(dept_name="Computer Science", head_of_dept="Dr. Alan Turing", budget=500000.00)
        dept_ee = Department(dept_name="Electrical Engineering", head_of_dept="Dr. Nikola Tesla", budget=450000.00)
        dept_math = Department(dept_name="Mathematics", head_of_dept="Dr. Carl Gauss", budget=300000.00)
        
        session.add_all([dept_cs, dept_ee, dept_math])
        session.commit()

        s1 = Student(first_name="Alice", last_name="Smith", email="alice.smith@university.edu", date_of_birth=date(2002, 5, 14), department_id=dept_cs.department_id, enrollment_year=2021)
        s2 = Student(first_name="Bob", last_name="Jones", email="bob.jones@university.edu", date_of_birth=date(2001, 8, 22), department_id=dept_cs.department_id, enrollment_year=2020)
        s3 = Student(first_name="Charlie", last_name="Brown", email="charlie.brown@university.edu", date_of_birth=date(2003, 1, 10), department_id=dept_ee.department_id, enrollment_year=2022)
        s4 = Student(first_name="Diana", last_name="Prince", email="diana.prince@university.edu", date_of_birth=date(2002, 11, 30), department_id=dept_math.department_id, enrollment_year=2021)
        s5 = Student(first_name="Evan", last_name="Wright", email="evan.wright@university.edu", date_of_birth=date(2001, 3, 18), department_id=dept_cs.department_id, enrollment_year=2020)

        session.add_all([s1, s2, s3, s4, s5])
        session.commit()
        print("Inserted 3 Departments and 5 Students successfully.")

        print("\n--- TASK 2.82: INSERT Courses and Enrollments ---")
        c1 = Course(course_name="Data Structures & Algorithms", course_code="CS101", credits=4, department_id=dept_cs.department_id)
        c2 = Course(course_name="Database Management Systems", course_code="CS201", credits=3, department_id=dept_cs.department_id)
        c3 = Course(course_name="Circuit Analysis", course_code="EE101", credits=4, department_id=dept_ee.department_id)

        session.add_all([c1, c2, c3])
        session.commit()

        e1 = Enrollment(student_id=s1.student_id, course_id=c1.course_id, enrollment_date=date(2023, 9, 1), grade="A")
        e2 = Enrollment(student_id=s1.student_id, course_id=c2.course_id, enrollment_date=date(2023, 9, 1), grade="A-")
        e3 = Enrollment(student_id=s2.student_id, course_id=c1.course_id, enrollment_date=date(2023, 9, 1), grade="B+")
        e4 = Enrollment(student_id=s3.student_id, course_id=c3.course_id, enrollment_date=date(2023, 9, 1), grade="A")

        session.add_all([e1, e2, e3, e4])
        session.commit()
        print("Inserted 3 Courses and 4 Enrollments successfully.")

        print("\n--- TASK 2.83: READ - Students in 'Computer Science' ---")
        cs_students = session.query(Student).join(Department).filter(Department.dept_name == 'Computer Science').all()
        for student in cs_students:
            print(f"CS Student: {student.first_name} {student.last_name} | Email: {student.email}")

        print("\n--- TASK 2.84: READ - All Enrollments (Demonstrating N+1 Query Problem) ---")
        enrollments = session.query(Enrollment).all()
        print(f"Retrieved {len(enrollments)} enrollment records. Iterating through relationships...")
        for enr in enrollments:
            # Accessing .student and .course lazily triggers separate SQL queries for each iteration
            print(f"Student: {enr.student.first_name} {enr.student.last_name} | Course: {enr.course.course_name} | Grade: {enr.grade}")

        print("\n--- TASK 2.85: UPDATE - Student Enrollment Year by Email ---")
        target_student = session.query(Student).filter(Student.email == "alice.smith@university.edu").first()
        if target_student:
            print(f"Original enrollment_year for Alice: {target_student.enrollment_year}")
            target_student.enrollment_year = 2022
            session.commit()
            print(f"Updated enrollment_year for Alice: {target_student.enrollment_year}")

        print("\n--- TASK 2.86: DELETE - Remove an Enrollment Record ---")
        enrollment_to_delete = session.query(Enrollment).filter(Enrollment.enrollment_id == e4.enrollment_id).first()
        if enrollment_to_delete:
            session.delete(enrollment_to_delete)
            session.commit()
            print(f"Enrollment ID {e4.enrollment_id} deleted successfully.")
        
        remaining_count = session.query(Enrollment).count()
        print(f"Remaining Enrollments count: {remaining_count}")

    except Exception as e:
        session.rollback()
        print(f"Error during CRUD operations: {e}")
        raise
    finally:
        session.close()


# ------------------------------------------------------------------------------
# TASK 3: Eager Loading to Fix N+1
# ------------------------------------------------------------------------------

def run_eager_loading_demo():
    session = Session()
    try:
        print("\n--- TASK 3.88: READ - All Enrollments with joinedload (Fixing N+1) ---")
        # joinedload executes a single JOIN query loading Enrollment, Student, and Course together
        eager_enrollments = session.query(Enrollment).options(
            joinedload(Enrollment.student),
            joinedload(Enrollment.course)
        ).all()
        
        print(f"Retrieved {len(eager_enrollments)} enrollment records in 1 SQL query with joinedload.")
        for enr in eager_enrollments:
            print(f"Student: {enr.student.first_name} {enr.student.last_name} | Course: {enr.course.course_name} | Grade: {enr.grade}")

    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    run_crud_operations()
    run_eager_loading_demo()
