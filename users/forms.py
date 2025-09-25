from django import forms
from .models import Goods, Cart

class CartForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Goods.objects.all())
    quantity = forms.IntegerField(min_value=0)

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