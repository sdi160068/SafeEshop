from typing import Any
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render

from auth.jwt import decode_jwt
from auth.models import Token
from eshop.forms import ProductForm
from eshop.models import Cart, OrderedProduct, Product

def index(request):
    search = request.GET.get('search', None)
    token = request.COOKIES.get('jwt_token')
    token_obj = Token.objects.filter(token=token).first()

    if token_obj == None :
        return HttpResponseNotFound()

    payload = decode_jwt(token)

    if payload != None :
        if search == None or search == '':
            products = Product.objects.all()
            all = True
        else:
            products = Product.objects.filter(name__contains=search)
            all = False

        cart = Cart.objects.filter(user_id= payload["id"] ).first()

        return render(request,'index.html', context={"products": products, "cart" : cart, 'all' : all})
    return HttpResponseNotFound()

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
    token = request.COOKIES.get('jwt_token')
    payload = decode_jwt(token)

    if payload == None :
        return HttpResponseNotFound()

    cart = Cart.objects.filter(user_id=payload["id"]).first()
    if cart == None:
        cart = Cart(
            user_id = payload["id"]
        )
        cart.save()

    oProduct = OrderedProduct.objects.filter(product_id=id).first()
    if( oProduct == None):
        oProductTmp = OrderedProduct(
            product_id = id,
            cart_id = cart.id,
            quantity = 1,
        )

        oProductTmp.save()
    else:
        oProduct.quantity += 1
        oProduct.save()
    return redirect("eshop:index")


def payment(request):
    token = request.COOKIES.get('jwt_token')
    payload = decode_jwt(token)

    if payload == None :
        return HttpResponseNotFound()
    
    cart = Cart.objects.filter(user_id=payload["id"]).first()
    if cart == None:
        return HttpResponseRedirect("/eshop/")

    return render(request,'payment.html', context={"cart" : cart})