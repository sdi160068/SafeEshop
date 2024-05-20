from django import forms

class LoginForm(forms.Form) :
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", max_length=100)

class RegisterForm(forms.Form) :
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", max_length=100)
    confirm_password = forms.CharField(label="password", max_length=100)