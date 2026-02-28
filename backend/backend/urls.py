"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import List
from django.contrib import admin
from django.urls import path
from students.schema import CreateStudent, ReadStudent
from ninja import NinjaAPI
from students.models import Student

api = NinjaAPI()

@api.get("/test")
def status(request):
    return {"status": "ok"}


# Students
@api.get("/students", response=List[ReadStudent])
def get_students(request):
    students = Student.objects.all()
    return students

@api.post("/students")
def create_student(request, data: CreateStudent):
    student = Student.objects.create(
        name=data.name
    )
    return student.user_id

# Courses

@api.get("/students/{student_id}/courses")
def get_student_courses(request, student_id: str):
    student = Student.objects.get(user_id=student_id)
    courses = student.courses.all()
    return courses

@api.post("/students/{student_id}/courses")
def create_student_course(request, student_id: str, data: dict):
    student = Student.objects.get(user_id=student_id)
    course = student.courses.create(name=data.name)
    return course.id

# Assignments




urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", api.urls)
]
