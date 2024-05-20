from django.contrib import messages
import auth.jwt as jwt
from auth.models import Token, User
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
            if user != None and check_password(form.data["password"],user.password):
                token = request.COOKIES.get('jwt_token')
                payload = jwt.decode_jwt(token)

                if payload == None :
                    token = jwt.encode_jwt({'id': str(user.id), 'username': user.username})

                    token_save = Token(
                        token = token
                    )

                    token_save.save()

                response = HttpResponseRedirect('/eshop/')

                response.set_cookie('jwt_token', token)

                return response
            else: 
                messages.error(message='The username or the password are incorrect.',request=request)
    return redirect('/')



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid() and form.data["password"] == form.data["confirm_password"]:
            user = User(username= form.data["username"], password = make_password(form.data["password"]))
            user.save()
    return HttpResponseRedirect("/")
