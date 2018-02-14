from django.db import models
from datetime import datetime

class MailBox(models.Model):
    serial_id = models.IntegerField(default=0)
    mailcount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.serial_id)

class DeliveredPost(models.Model):
    delivery_time = models.DateTimeField(default=datetime.now, blank=True)
    mailBox = models.ForeignKey(MailBox, on_delete=models.CASCADE, default=0)


class MailCollected(models.Model):
    collection_time = models.DateTimeField(default=datetime.now, blank=True)
    mailBox = models.ForeignKey(MailBox, on_delete=models.CASCADE, default=0)
