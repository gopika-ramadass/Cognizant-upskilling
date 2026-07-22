import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from courses.models import Department, Course, Student, Enrollment
from courses.views import CourseListView, CourseDetailView, CourseViewSet

def test_api():
    print("=== Task 1 & 2: Testing DRF Views & ViewSets ===")
    factory = APIRequestFactory()

    # Reset data
    Enrollment.objects.all().delete()
    Student.objects.all().delete()
    Course.objects.all().delete()
    Department.objects.all().delete()

    dept = Department.objects.create(name='Computer Science', head_of_dept='Alan Turing', budget=50000)

    # 1. Test CourseListView POST
    request = factory.post('/api/fbv-courses/', {'name': 'Data Structures', 'code': 'CS101', 'credits': 4, 'department': dept.id}, format='json')
    response = CourseListView.as_view()(request)
    print("1. CourseListView POST status:", response.status_code, "Data:", response.data)
    assert response.status_code == 201

    course_id = response.data['id']

    # 2. Test CourseListView GET
    request = factory.get('/api/fbv-courses/')
    response = CourseListView.as_view()(request)
    print("2. CourseListView GET status:", response.status_code, "Count:", len(response.data))
    assert response.status_code == 200

    # 3. Test CourseDetailView GET & PUT
    request = factory.get(f'/api/fbv-courses/{course_id}/')
    response = CourseDetailView.as_view()(request, pk=course_id)
    print("3. CourseDetailView GET status:", response.status_code, "Name:", response.data['name'])
    assert response.status_code == 200

    request = factory.put(f'/api/fbv-courses/{course_id}/', {'name': 'Advanced Data Structures', 'code': 'CS101', 'credits': 4, 'department': dept.id}, format='json')
    response = CourseDetailView.as_view()(request, pk=course_id)
    print("4. CourseDetailView PUT status:", response.status_code, "Updated Name:", response.data['name'])
    assert response.status_code == 200

    # Create Student & Enrollment for custom action test
    student = Student.objects.create(first_name='John', last_name='Doe', email='john@example.com', department=dept, enrollment_year=2024)
    course_obj = Course.objects.get(id=course_id)
    Enrollment.objects.create(student=student, course=course_obj)

    # 5. Test Custom Action GET /api/courses/{id}/students/
    request = factory.get(f'/api/courses/{course_id}/students/')
    response = CourseViewSet.as_view({'get': 'students'})(request, pk=course_id)
    print("5. Custom Action /courses/{id}/students/ status:", response.status_code)
    print("   Enrolled Students:", [s['first_name'] + ' ' + s['last_name'] for s in response.data])
    assert response.status_code == 200
    assert len(response.data) == 1

    print("\nALL DRF TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_api()
