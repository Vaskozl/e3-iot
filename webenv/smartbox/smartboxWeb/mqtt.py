import paho.mqtt.client as mqtt
import json

from smartboxWeb.models import MailBox, DeliveredPost, MailCollected

# Topics
# Publish esys/group_num/serial_number/door
# Subscribe esys/group_num/{collection | delivery}

def on_connect(mqtt, obj, flags, rc):
    print("Connected " + str(rc))

# On message store event in relavent database and change mailcount accordinly
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    serial_id = payload['serial_id']
    print(serial_id)
    if not MailBox.objects.filter(serial_id = serial_id):
            mailBox = MailBox(serial_id = serial_id)
            mailBox.save()
    mailBox = MailBox.objects.filter(serial_id = serial_id)[0]
    print('Mailcount: ' + str(mailBox.mailcount))
    if msg.topic == "esys/VKPD/collection":
        mailBox.mailcount = 0
        collection = MailCollected(mailBox = mailBox)
        print("Collection")
        collection.save()
    elif msg.topic == "esys/VKPD/delivery":
        print("Delivery")
        mailBox.mailcount = payload['mail_count']
        delivery = DeliveredPost(mailBox = mailBox)
        delivery.save()
    mailBox.save()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.10", 1883, 60)
client.subscribe([("esys/VKPD/collection", 0), ("esys/VKPD/delivery", 0)])
