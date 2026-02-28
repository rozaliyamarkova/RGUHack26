from django.db import models

# Create your models here.

class BusStop(models.Model):
    ATCOCode = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    indicator = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    active = models.CharField(max_length=255)
