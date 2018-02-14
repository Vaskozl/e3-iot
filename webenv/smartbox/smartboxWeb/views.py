from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from smartboxWeb.models import MailBox, DeliveredPost, MailCollected

def index(request):
    return render(request, 'smartboxWeb/index.html')

def login(request):
    return render(request, 'smartboxWeb/login.html')


def get_last_delivery_time(serialID):
    latest_deliveries = DeliveredPost.objects.all().order_by('-delivery_time')
    for delivery in latest_deliveries:
        if(str(delivery.mailBox.serial_id) == serialID):
            return delivery.delivery_time.strftime("%H:%M %d-%m-%Y")
    return 'No Delivered Mail';

def get_last_collection_time(serialID):
    latest_collections = MailCollected.objects.all().order_by('-collection_time')
    for collection in latest_collections:
        if(str(collection.serial.serial_id) == serialID):
            return collection.collection_time.strftime("%H:%M %d-%m-%Y")
    return 'No Collected Mail';


def data(request):
    try:
        post = request.POST['serialID']
        request.session['serial_id'] = post
    except (KeyError):
        print("No post")
    serialID = request.POST['serialID']
    if not MailBox.objects.filter(serial_id = serialID):
        mailBox = MailBox(serial_id=serialID)
        mailBox.save()
    context = {'serial_id' : serialID,
                'last_delivery_time': get_last_delivery_time(serialID),
                'last_collection_time': get_last_collection_time(serialID),
                'mail_count': MailBox.mailcount()}
    return render(request, 'smartboxWeb/data.html', context)
