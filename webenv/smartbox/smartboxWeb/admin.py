from django.contrib import admin
from .models import Sensor, DeliveredPost, MailCollected

admin.site.register(Sensor)
admin.site.register(DeliveredPost)
admin.site.register(MailCollected)
# Register your models here.
