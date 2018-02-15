from django.contrib import admin
from .models import MailBox, DeliveredPost, MailCollected

admin.site.register(MailBox)
admin.site.register(DeliveredPost)
admin.site.register(MailCollected)
