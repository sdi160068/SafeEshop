from django.utils.crypto import get_random_string
from django.contrib import messages
import auth.jwt as jwt
from auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm, RegisterForm

def index(request):
    return render(request,'login.html')

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.data["username"]).first()
            
            response = HttpResponseRedirect('/eshop/')

            if user != None and custom_check_password(form.data["password"],user.password):
                token = request.COOKIES.get('jwt_token')

                payload = jwt.decode_jwt(token)

                if payload == None :
                    # token => token for authentication and exp => expiration date of toiken , for cookie
                    token, exp = jwt.encode_jwt({'id': str(user.id), 'username': user.username})

                    response.set_cookie('jwt_token', token , expires=exp)

                return response
            else: 
                messages.error(message='The username or the password are incorrect.',request=request)
        else: 
            messages.error(message='The username or the password are incorrect.',request=request)
    return redirect('/')

def custom_check_password(password, stored_password):
    try: 
        stored_salt, actual_password = stored_password.split(':')

        hashed_password_to_check = make_password(password, salt=stored_salt, hasher='argon2')

        return actual_password == hashed_password_to_check
    except Exception :
        return False

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid() and form.data["password"] == form.data["confirm_password"]:

            salt = get_random_string(length=12)

            password = salt + ":"+ make_password(form.data["password"],salt=salt,hasher="argon2")
            user = User(username= form.data["username"], password = password)
            user.save()
    return HttpResponseRedirect("/")
