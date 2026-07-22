# Role: Root URL dispatcher mapping URL patterns to view functions or delegating to app-level urlconfs.
"""
URL configuration for coursemanager project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),
]
