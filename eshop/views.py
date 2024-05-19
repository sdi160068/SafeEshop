from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from eshop.forms import ProductForm
from eshop.models import Cart, OrderedProduct, Product

def index(request):
    products = Product.objects.all()
    cart = Cart.objects.filter(user_id='8e0fce3b8eb149f49d2dda3cd07dfa48').last()
    return render(request,'index.html', context={"products": products, "cart" : cart})

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

def add_to_cart(request, id):
    oProduct = OrderedProduct.objects.filter(product_id=id).first()
    if( oProduct == None):
        cart = Cart(
            user_id = '8e0fce3b8eb149f49d2dda3cd07dfa48'
        )
        cart.save()

        oProductTmp = OrderedProduct(
            product_id = id,
            cart_id = cart.id,
            quantity = 1,
        )

        oProductTmp.save()
    return redirect("eshop:index")
