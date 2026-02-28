from django.db import models
from students.models import Student

# Create your models here.

class Course(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=255)
