from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from smartboxWeb.models import MailBox, DeliveredPost, MailCollected
import paho.mqtt.publish as publish


def index(request):
    return render(request, 'smartboxWeb/index.html')

def login(request):
    return render(request, 'smartboxWeb/login.html')

# Get the latest delivery event time
def get_last_delivery_time(serialID):
    latest_deliveries = DeliveredPost.objects.all().order_by('-delivery_time')
    for delivery in latest_deliveries:
        if(str(delivery.mailBox.serial_id) == serialID):
            return delivery.delivery_time.strftime("%H:%M:%S %d-%m-%Y")
    return 'No Delivered Mail';

# Get the latest collection event time
def get_last_collection_time(serialID):
    latest_collections = MailCollected.objects.all().order_by('-collection_time')
    for collection in latest_collections:
        if(str(collection.mailBox.serial_id) == serialID):
            return collection.collection_time.strftime("%H:%M:%S %d-%m-%Y")
    return 'No Collected Mail';

# Get an array of all the delivery event times for a mailbox with serialID
def get_delivery_times(serialID):
    delivery_times = [0] * 24
    deliveries = DeliveredPost.objects.filter(mailBox__serial_id = serialID)
    for delivery in deliveries:
        hour = int(delivery.delivery_time.strftime("%H"))
        delivery_times[hour] += 1
    return delivery_times

# Pass the data for a mailbox to the data template
def data(request):
    try:
        post = request.POST['serialID']
        request.session['serial_id'] = post
    except (KeyError):
        print("No post")
    serialID = request.session['serial_id']
    if not MailBox.objects.filter(serial_id = serialID):
        mailBox = MailBox(serial_id=serialID)
        mailBox.save()
    context = {'serial_id' : serialID,
                'last_delivery_time': get_last_delivery_time(serialID),
                'last_collection_time': get_last_collection_time(serialID),
                'mailcount': MailBox.objects.filter(serial_id = serialID)[0].mailcount,
                'times' : get_delivery_times(serialID)}
    return render(request, 'smartboxWeb/data.html', context)

# On button press publish for the mailbox with serialID to toggle door
def send_door_request(request):
    topic = 'esys/VKPD/' + str(request.session['serial_id'])
    publish.single(topic, hostname="192.168.0.10", port=1883)

# Check if there are newer times for delivery or collection than are being displayed
# if so tell the client
def is_updated(request):
    last_client_delivery_time = request.GET.get('last_delivery_time', None)
    last_client_collection_time = request.GET.get('last_collection_time', None)
    serialID = request.session['serial_id']
    if (get_last_delivery_time(serialID) > last_client_delivery_time) or \
            (get_last_collection_time(serialID) > last_client_collection_time):
        return JsonResponse({'client_is_old': True})
    return JsonResponse({'client_is_old': False})
