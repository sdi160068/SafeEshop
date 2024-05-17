from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('add_product', views.add_product),
]