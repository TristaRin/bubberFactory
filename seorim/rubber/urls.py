from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('hello_world',views.hello_world), 
    url('getGantt', views.getGantt),
]
