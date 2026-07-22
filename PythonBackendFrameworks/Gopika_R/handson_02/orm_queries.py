import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
django.setup()

from django.db import connection, reset_queries
from django.db.models import Count, F
from courses.models import Department, Course, Student, Enrollment

def run_orm_demo():
    print("=== Task 2: Django ORM Queries Demo ===")

    # Clear existing data for clean run
    Enrollment.objects.all().delete()
    Student.objects.all().delete()
    Course.objects.all().delete()
    Department.objects.all().delete()

    # Step 16: Create at least 2 Department, 4 Course, and 5 Student objects
    cs_dept = Department.objects.create(name='Computer Science', head_of_dept='Dr. Alan Turing', budget=50000.00)
    ee_dept = Department.objects.create(name='Electrical Engineering', head_of_dept='Dr. Nikola Tesla', budget=45000.00)

    c1 = Course.objects.create(name='Data Structures', code='CS101', credits=4, department=cs_dept)
    c2 = Course.objects.create(name='Algorithms', code='CS102', credits=4, department=cs_dept)
    c3 = Course.objects.create(name='Circuit Analysis', code='EE101', credits=3, department=ee_dept)
    c4 = Course.objects.create(name='Digital Signal Processing', code='EE102', credits=4, department=ee_dept)

    s1 = Student.objects.create(first_name='Alice', last_name='Smith', email='alice@example.com', department=cs_dept, enrollment_year=2024)
    s2 = Student.objects.create(first_name='Bob', last_name='Jones', email='bob@example.com', department=cs_dept, enrollment_year=2024)
    s3 = Student.objects.create(first_name='Charlie', last_name='Brown', email='charlie@example.com', department=cs_dept, enrollment_year=2023)
    s4 = Student.objects.create(first_name='David', last_name='Miller', email='david@example.com', department=ee_dept, enrollment_year=2024)
    s5 = Student.objects.create(first_name='Eve', last_name='Wilson', email='eve@example.com', department=ee_dept, enrollment_year=2023)

    print(f"Created {Department.objects.count()} departments, {Course.objects.count()} courses, {Student.objects.count()} students.")

    # Step 17: Query all courses in 'Computer Science' using double underscore (department__name)
    cs_courses = Course.objects.filter(department__name='Computer Science')
    print("\n[Step 17] Courses in Computer Science:")
    for course in cs_courses:
        print(f"  - {course.code}: {course.name}")

    # Step 18: Use .values() and .annotate() to count courses per department
    dept_course_counts = Department.objects.annotate(course_count=Count('courses')).values('name', 'course_count')
    print("\n[Step 18] Course count per department:")
    for row in dept_course_counts:
        print(f"  - {row['name']}: {row['course_count']} course(s)")

    # Step 19: Use select_related to fetch students along with department in a single query
    reset_queries()
    students_with_dept = list(Student.objects.select_related('department').all())
    print("\n[Step 19] Students with Department (using select_related):")
    for student in students_with_dept:
        print(f"  - {student.first_name} {student.last_name} ({student.department.name})")
    print(f"Executed SQL Queries Count: {len(connection.queries)}")

    # Step 20: Perform F() expression update: increase budget by 10%
    print("\n[Step 20] Updating department budgets by 10% using F() expression...")
    Department.objects.update(budget=F('budget') * 1.10)
    for dept in Department.objects.all():
        print(f"  - {dept.name} updated budget: ${dept.budget:.2f}")

if __name__ == '__main__':
    run_orm_demo()
