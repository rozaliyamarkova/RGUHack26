from django.db import models
import uuid

# Create your models here.

class Student(models.Model):
    user_id = models.CharField(max_length=255, unique=True,default = uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name