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
from assignments.schema import ReadAssignment, CreateAssignmentLog, ReadAssignmentLog, CreateAssignment
from assignments.models import Assignment
from courses.schema import CreateCourse, ReadCourse
from students.schema import CreateStudent, CreateStudentResponse, ReadStudent
from ninja import NinjaAPI
from students.models import Student
from ninja.security import HttpBearer


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            student = Student.objects.get(user_id=token)
            return student
        except Student.DoesNotExist:
            return None
        

api = NinjaAPI(auth=AuthBearer())

from bustops.find_closest import find_closest_bus_stops
from bustops.get_live_time import fetch_from_traveline_api
from bustops.scheme import ReadBusStop, Bus

from django.conf import settings


from typing import List

@api.get("/test")
def status(request):
    return {"status": "ok"}


# Students
@api.get("/students", response=List[ReadStudent])
def get_students(request):
    students = Student.objects.all()
    return students

@api.post("/students", auth=None, response=CreateStudentResponse)
def create_student(request, data: CreateStudent):
    student = Student.objects.create(
        name=data.name
    )
    return student

@api.get("/students/me", response=ReadStudent)
def get_current_student(request):
    return request.auth

# Courses

@api.get("/courses", response=List[ReadCourse])
def get_student_courses(request):
    courses = request.auth.courses.all()
    return courses

@api.post("/courses", response=ReadCourse)
def create_student_course(request, data: CreateCourse):
    course = request.auth.courses.create(name=data.name)
    return course

@api.delete("/courses/{course_id}")
def delete_student_course(request, course_id: int):
    course = request.auth.courses.get(id=course_id)
    course.delete()
    return {"status": "deleted"}

# Assignments

@api.get("/courses/{course_id}/assignments", response=List[ReadAssignment])
def get_course_assignments(request, course_id: int):
    course = request.auth.courses.get(id=course_id)
    assignments = course.assignments.all()
    return assignments

@api.post("/courses/{course_id}/assignments", response=ReadAssignment)
def create_course_assignment(request, course_id: int, data: CreateAssignment):
    course = request.auth.courses.get(id=course_id)
    assignment = course.assignments.create(name=data.name, description=data.description)
    return assignment

@api.delete("/assignments/{assignment_id}")
def delete_course_assignment(request, assignment_id: int):
    assignment = Assignment.objects.filter(course__student=request.auth, id=assignment_id).first()
    assignment.delete()
    return {"status": "deleted"}

# Assignment log
@api.post("/assignments/{assignment_id}/logs", response=ReadAssignmentLog)
def create_assignment_log(request, assignment_id:int, data: CreateAssignmentLog):
    assignment = Assignment.objects.filter(course__student=request.auth, id=assignment_id).first()
    log = assignment.logs.create(time_spent=data.time_spent, log_date=data.log_date)
    return log

@api.get("/assignments/{assignment_id}/logs", response=List[ReadAssignmentLog])
def get_assignment_logs(request, assignment_id:int):
    assignment = Assignment.objects.filter(course__student=request.auth, id=assignment_id).first()
    logs = assignment.logs.all()
    return logs

@api.get("/closest_busses", response=List[ReadBusStop])
def status(request):
    return find_closest_bus_stops("""57Â°7'7.2"N""", """2Â°8'4.3"W""")

@api.get("/bus/{stop_id}", response=List[Bus])
def bus_api(request, stop_id):
    global daily_bus_request_count
    all_buses = []

    stop_data = fetch_from_traveline_api(stop_id, settings.BUS_API_USERNAME, settings.BUS_API_PASSWORD)
    print(stop_data)
    
        

    for bus in stop_data:
        all_buses.append(bus)
    
    # Sort all buses by departure time
    all_buses.sort(key=lambda x: x['departure_time'])
    
    return all_buses

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", api.urls)
]

