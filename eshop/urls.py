from django.urls import path

from . import views

app_name = 'eshop'

urlpatterns = [
    path('', views.index, name="index"),
    path('add-product/', views.add_product,name='add_product'),
    path('add-to-cart/<id>/', views.add_to_cart,name='add_to_cart'),
    path('payment/', views.payment,name='payment'),
]