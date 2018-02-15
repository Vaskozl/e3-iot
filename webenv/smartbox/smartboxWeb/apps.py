from django.apps import AppConfig


class SmartboxwebConfig(AppConfig):
    name = 'smartboxWeb'

    def ready(self):
        from . import mqtt
        #mqtt.client.loop_start()
