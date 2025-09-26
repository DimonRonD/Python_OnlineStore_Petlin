from django import forms
from .models import Goods, Cart

class CartForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Goods.objects.all())
    quantity = forms.IntegerField(min_value=0)
    customer_id = forms.IntegerField(widget=forms.HiddenInput())

class OrderForm(forms.Form):
    # name = forms.CharField()
    # address = forms.CharField()
    # email = forms.EmailField()
    # cart = forms.ModelChoiceField(queryset=Cart.objects.all())
    customer_id = forms.IntegerField(widget=forms.HiddenInput())

class ToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=0)

class LoginForm(forms.Form):
    calendar = forms.CharField(label="calendar", max_length=100)

class RegisterForm(forms.Form):
    customer_name = forms.CharField(max_length=50)
    customer_surname = forms.CharField(max_length=50)
    customer_patronym = forms.CharField(max_length=100)
    customer_address = forms.CharField(max_length=300)
    customer_email = forms.EmailField()
    customer_phone = forms.CharField(max_length=15)
    customer_password = forms.CharField(max_length=10, widget=forms.PasswordInput())