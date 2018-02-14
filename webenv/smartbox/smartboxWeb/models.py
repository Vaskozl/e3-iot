from django.db import models
from datetime import datetime

class Sensor(models.Model):
    sensor_id = models.IntegerField(default=0)

class DeliveredPost(models.Model):
    delivery_time = models.DateTimeField(default=datetime.now, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, default=0)

class MailCollected(models.Model):
    collection_time = models.DateTimeField(default=datetime.now, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, default=0)
