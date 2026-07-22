from django.http import HttpResponse

# Hello view returning API status message
def hello_view(request):
    return HttpResponse("Course Management API is running")
