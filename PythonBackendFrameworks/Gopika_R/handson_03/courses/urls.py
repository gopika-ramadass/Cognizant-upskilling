from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CourseListView,
    CourseDetailView,
    DepartmentViewSet,
    CourseViewSet,
    StudentViewSet,
    EnrollmentViewSet
)

# Task 2: Router Configuration
router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('courses', CourseViewSet)
router.register('students', StudentViewSet)
router.register('enrollments', EnrollmentViewSet)

urlpatterns = [
    # Task 1: APIView route patterns
    path('fbv-courses/', CourseListView.as_view(), name='course-list-view'),
    path('fbv-courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail-view'),

    # Task 2: ViewSet router pattern (handles /courses/, /courses/{id}/, /courses/{id}/students/)
    path('', include(router.urls)),
]
