from django.contrib import admin
from .models import MailBox, DeliveredPost, MailCollected

# Allow models to be altered on the admin pane
admin.site.register(MailBox)
admin.site.register(DeliveredPost)
admin.site.register(MailCollected)
