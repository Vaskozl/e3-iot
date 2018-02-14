from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def index(request):
    return render(request, 'smartboxWeb/index.html')

def login(request):
    return render(request, 'smartboxWeb/login.html')

def data_confirm(request):
    sensor_id = request.POST['sensorID']
    return HttpResponseRedirect(reverse('data', args=(sensor_id,)))

def data(request, sensor_id):
    context = {'sensor_id' : sensor_id}
    return render(request, 'smartboxWeb/data.html', context)
