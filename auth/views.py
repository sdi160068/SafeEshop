from django.contrib import messages
import auth.jwt as jwt
from auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm

def index(request):
    return render(request,'login.html')

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.data["username"]).first()
            
            response = HttpResponseRedirect('/eshop/')

            if user != None and check_password(form.data["password"],user.password):
                token = request.COOKIES.get('jwt_token')

                payload = jwt.decode_jwt(token)

                if payload == None :
                    # token => token for authentication and exp => expiration date of toiken , for cookie
                    token, exp = jwt.encode_jwt({'id': str(user.id), 'username': user.username})

                    response.set_cookie('jwt_token', token , expires=exp)

                return response
            else: 
                messages.error(message='The username or the password are incorrect.',request=request)
    return redirect('/')
