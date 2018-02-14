from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='root'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('data/', views.data, name='data'),
]
