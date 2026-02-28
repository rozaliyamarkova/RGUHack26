from django.db import models
from courses.models import Course

# Create your models here.

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    weighting = models.FloatField(help_text="Weighting of the assignment towards the final grade (e.g., 0.2 for 20%)")
    grade = models.FloatField(help_text="Grade received for the assignment (e.g., 85.5)", null=True, blank=True)

    time_needed = models.IntegerField(help_text="Estimated time needed to complete the assignment in minutes")
    time_estimated = models.IntegerField(help_text="Estimated time by ai complete the assignment in minutes", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AssignmentLog(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='logs')
    duration = models.IntegerField(help_text="Time spent on the assignment in minutes",blank=True, null=True)

    note = models.TextField(help_text="Optional note of what was achieved", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.duration} minutes"

class AssignmentNote(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField(help_text="Note for the assignment")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.assignment.title}"