from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render

from auth.jwt import decode_jwt, validate_token
from auth.models import Token, User
from eshop.forms import ProductForm
from eshop.models import Cart, OrderedProduct, Product

def index(request):
    search = request.GET.get('search', None)
    token = request.headers.get('Authorization')
                
    if token and token.startswith('Bearer '):
        token = token[7:]
    # token = request.COOKIES.get('jwt_token')
   
    payload = validate_token(token)

    if payload != None :
        if search == None or search == '':
            products = Product.objects.all()
            all = True
        else:
            products = Product.objects.filter(name__contains=search)
            all = False

        cart = Cart.objects.filter(user_id= payload["id"], paid = False).first()
        if cart != None:
            op = cart.getProducts()

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
   
    payload = validate_token(token)

    if payload == None :
        return HttpResponseNotFound()

    # 9fd779f68ffb4191ac72aea73fb9ddaf
    cart = Cart.objects.filter(user_id=payload["id"], paid=False).first()
    if cart == None:
        cart = Cart(
            user_id = payload["id"]
        )
        cart.save()

    oProduct = OrderedProduct.objects.filter(product_id=id, cart_id=cart.id).first()
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
    # return redirect("eshop:index")
    return HttpResponseRedirect("/eshop/")

def add_address(request):
    token = request.COOKIES.get('jwt_token')
   
    payload = validate_token(token)

    if payload == None :
        return HttpResponseNotFound()
    
    cart = Cart.objects.filter(user_id=payload["id"], paid=False).first()
    if cart == None:
        return HttpResponseRedirect("/eshop/")
    
    if cart.address != "":
        return HttpResponseRedirect("/eshop/payment/")
    
    cart.address = request.POST.get("address")
    cart.save()

    return HttpResponseRedirect("/eshop/payment/")

def payment(request):
    token = request.COOKIES.get('jwt_token')
    payload = decode_jwt(token)

    if payload == None :
        return HttpResponseNotFound()

    cart = Cart.objects.filter(user_id=payload["id"], paid=False).first()
    if cart == None:
        return HttpResponseRedirect("/eshop/")

    return render(request,'payment.html', context={"cart" : cart})

def change_info(request):
    token = request.COOKIES.get('jwt_token')
   
    payload = validate_token(token)

    if payload == None :
        return HttpResponseNotFound()
    
    cart = Cart.objects.filter(user_id=payload["id"], paid=False).first()
    if cart == None:
        return HttpResponseRedirect("/eshop/")

    cart.address = ""
    cart.save()

    return HttpResponseRedirect("/eshop/payment/")

def complete_payment(request):
    token = request.COOKIES.get('jwt_token')
    payload = decode_jwt(token)

    if payload == None :
        return HttpResponseNotFound()

    user = User.objects.filter(id=payload["id"]).first()
    cart = Cart.objects.filter(user_id=payload["id"],paid=False).first()
    if cart == None:
        return HttpResponseRedirect("/eshop/")
        
    cart.paid = True
    cart.save()

    return render(request,'complete_payment.html', context={"cart" : cart, "user" : user})