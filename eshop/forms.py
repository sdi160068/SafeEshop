from django import forms

class ProductForm(forms.Form) :
    name = forms.CharField(label="name", max_length=100)
    price = forms.CharField(label="price", max_length=100)