from django.db import models
import datetime
from django.utils import timezone

class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    visitor_name = models.CharField(max_length=50)
    visitor_email = models.EmailField(blank=True, null=True)
    visitor_phone = models.CharField(max_length=15)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='meetings')  # Add related_name
    date = models.DateTimeField(default=timezone.now)
    time_in = models.TimeField(default=datetime.datetime.now())
    time_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.visitor_name}"

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=50)
    doctor_email = models.EmailField(blank=True, null=True)
    doctor_phone = models.CharField(max_length=15)
    doctor_image = models.ImageField(upload_to='static/media', null=True, blank=True)
    doctor_desc = models.CharField(max_length=50)
    address = models.CharField(max_length=100, default="HealthPlus, Rohini-22, New Delhi")
    status = models.BooleanField(default=True)
    available = models.CharField(max_length=50, default='')
    current_meeting_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.doctor_name}"
