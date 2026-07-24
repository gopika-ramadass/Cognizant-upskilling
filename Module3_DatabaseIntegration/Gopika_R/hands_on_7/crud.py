"""
================================================================================
DIGITAL NURTURE 5.0 | MODULE 3: DATABASE INTEGRATION
HANDS-ON 7: Task 2 & 3 - CRUD Operations & Eager Loading (Fixing N+1)
================================================================================

TASK 3 FINDINGS & COMPARISON:
--------------------------------------------------------------------------------
1. N+1 Problem (Task 2 Step 84):
   - `session.query(Enrollment).all()` fetches N enrollment records (1 query).
   - Iterating over enrollments and accessing `.student` and `.course` fires
     1 query per student and 1 query per course for each row.
   - Result: 1 + 2*N queries issued (e.g., 9 queries for 4 enrollments, 25 for 12).

2. Eager Loading Fix (Task 3 Step 88):
   - `session.query(Enrollment).options(joinedload(Enrollment.student), joinedload(Enrollment.course)).all()`
   - SQLAlchemy constructs a single SELECT query with LEFT OUTER JOINs.
   - Result: 1 single query executed! Query count reduced from 9 (or 13/25) down to 1.

3. Django ORM Equivalent (Bonus Step 91):
   - `Enrollment.objects.select_related('student', 'course').all()`
================================================================================
"""

from datetime import date
from sqlalchemy.orm import sessionmaker, joinedload
from models import engine, Base, Department, Student, Course, Enrollment, Professor

Session = sessionmaker(bind=engine)

def run_crud_and_eager_loading():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()
    try:
        # INSERT Departments
        dept_cs = Department(dept_name="Computer Science", head_of_dept="Dr. Alan Turing", budget=500000.00)
        dept_ee = Department(dept_name="Electrical Engineering", head_of_dept="Dr. Nikola Tesla", budget=450000.00)
        dept_math = Department(dept_name="Mathematics", head_of_dept="Dr. Carl Gauss", budget=300000.00)
        session.add_all([dept_cs, dept_ee, dept_math])
        session.commit()

        # INSERT Students
        s1 = Student(first_name="Alice", last_name="Smith", email="alice.smith@university.edu", date_of_birth=date(2002, 5, 14), department_id=dept_cs.department_id, enrollment_year=2021)
        s2 = Student(first_name="Bob", last_name="Jones", email="bob.jones@university.edu", date_of_birth=date(2001, 8, 22), department_id=dept_cs.department_id, enrollment_year=2020)
        s3 = Student(first_name="Charlie", last_name="Brown", email="charlie.brown@university.edu", date_of_birth=date(2003, 1, 10), department_id=dept_ee.department_id, enrollment_year=2022)
        s4 = Student(first_name="Diana", last_name="Prince", email="diana.prince@university.edu", date_of_birth=date(2002, 11, 30), department_id=dept_math.department_id, enrollment_year=2021)
        s5 = Student(first_name="Evan", last_name="Wright", email="evan.wright@university.edu", date_of_birth=date(2001, 3, 18), department_id=dept_cs.department_id, enrollment_year=2020)
        session.add_all([s1, s2, s3, s4, s5])
        session.commit()

        # INSERT Courses
        c1 = Course(course_name="Data Structures & Algorithms", course_code="CS101", credits=4, department_id=dept_cs.department_id)
        c2 = Course(course_name="Database Management Systems", course_code="CS201", credits=3, department_id=dept_cs.department_id)
        c3 = Course(course_name="Circuit Analysis", course_code="EE101", credits=4, department_id=dept_ee.department_id)
        session.add_all([c1, c2, c3])
        session.commit()

        # INSERT Enrollments
        e1 = Enrollment(student_id=s1.student_id, course_id=c1.course_id, enrollment_date=date(2023, 9, 1), grade="A")
        e2 = Enrollment(student_id=s1.student_id, course_id=c2.course_id, enrollment_date=date(2023, 9, 1), grade="A-")
        e3 = Enrollment(student_id=s2.student_id, course_id=c1.course_id, enrollment_date=date(2023, 9, 1), grade="B+")
        e4 = Enrollment(student_id=s3.student_id, course_id=c3.course_id, enrollment_date=date(2023, 9, 1), grade="A")
        session.add_all([e1, e2, e3, e4])
        session.commit()

        print("\n=== READ: Computer Science Students ===")
        cs_students = session.query(Student).join(Department).filter(Department.dept_name == 'Computer Science').all()
        for s in cs_students:
            print(f"CS Student: {s.first_name} {s.last_name}")

        print("\n=== READ: Enrollments (Demonstrating N+1) ===")
        enrollments = session.query(Enrollment).all()
        for e in enrollments:
            print(f"Student: {e.student.first_name} | Course: {e.course.course_name}")

        print("\n=== UPDATE: Enrollment Year ===")
        target = session.query(Student).filter(Student.email == "alice.smith@university.edu").first()
        if target:
            target.enrollment_year = 2022
            session.commit()
            print(f"Updated Alice's enrollment_year to {target.enrollment_year}")

        print("\n=== DELETE: Enrollment ===")
        del_target = session.query(Enrollment).filter(Enrollment.enrollment_id == e4.enrollment_id).first()
        if del_target:
            session.delete(del_target)
            session.commit()
            print(f"Deleted enrollment ID {e4.enrollment_id}")

        print("\n=== READ: Enrollments with joinedload (Fixing N+1) ===")
        eager_enrollments = session.query(Enrollment).options(
            joinedload(Enrollment.student),
            joinedload(Enrollment.course)
        ).all()
        for e in eager_enrollments:
            print(f"Eager Loaded Student: {e.student.first_name} | Course: {e.course.course_name}")

    except Exception as err:
        session.rollback()
        print(f"Error: {err}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    run_crud_and_eager_loading()
