import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import IntegrityError
from courses.models import Department, Course, Student, Enrollment

def setup_admin_and_verify():
    # Step 21: Create superuser admin / admin@college.edu / Admin@123
    username = 'admin'
    email = 'admin@college.edu'
    password = 'Admin@123'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")

    # Step 25: Verify unique_together constraint on Enrollment
    dept, _ = Department.objects.get_or_create(name='CS Dept', head_of_dept='Head', budget=10000)
    course, _ = Course.objects.get_or_create(name='Test Course', code='TEST101', credits=3, department=dept)
    student, _ = Student.objects.get_or_create(first_name='John', last_name='Doe', email='john@example.com', department=dept, enrollment_year=2024)

    # First enrollment
    Enrollment.objects.filter(student=student, course=course).delete()
    Enrollment.objects.create(student=student, course=course)
    print("First enrollment created successfully.")

    # Second enrollment (should raise IntegrityError due to unique_together)
    try:
        Enrollment.objects.create(student=student, course=course)
        print("ERROR: Duplicate enrollment created without error!")
    except IntegrityError as e:
        print("SUCCESS: Duplicate enrollment caught by unique_together constraint as expected!")
        print(f"IntegrityError message: {e}")

if __name__ == '__main__':
    setup_admin_and_verify()
