from django.db import models

# Create your models here.

class BusStop(models.Model):
    ATCOCode = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    indicator = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    active = models.CharField(max_length=255)

class Bus(models.Model):
    line = models.CharField(max_length=255)
    operator = models.CharField(max_length=255)
    scheduled_time = models.CharField(max_length=255)
    departure_time = models.CharField(max_length=255)
    is_realtime = models.CharField(max_length=255)




    
