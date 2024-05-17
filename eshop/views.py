from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from eshop.forms import ProductForm
from eshop.models import Product

def index(request):
    products = Product.objects.all()
    return render(request,'index.html', context={"products": products})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid() \
            and form.data["name"] != None \
            and form.data["price"] != None :
            
            product = Product(
                name = form.data["name"],
                price = form.data["price"],
            )
            product.save()
    return HttpResponseRedirect("/eshop/")
