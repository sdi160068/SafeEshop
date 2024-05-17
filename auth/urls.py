from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.index),
    path('auth/login', views.login),
    path('auth/register', views.register),
]
