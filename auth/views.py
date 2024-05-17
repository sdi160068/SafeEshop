from auth.models import User
from django.shortcuts import render
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
                return HttpResponseRedirect("/eshop/")
    return HttpResponseRedirect("/")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid() and form.data["password"] == form.data["confirm_password"]:
            user = User(username= form.data["username"], password = make_password(form.data["password"]))
            user.save()
    return HttpResponseRedirect("/")
