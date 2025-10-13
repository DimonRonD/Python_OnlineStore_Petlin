from django import forms
from django.forms import ModelForm
from .models import Good, Customer

class CartForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Good.objects.all())
    quantity = forms.IntegerField(min_value=0)

class OrderForm(forms.Form):
    customer_id = forms.IntegerField(widget=forms.HiddenInput())

class ToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=0)

"""
    Логин передан на стандартного пользователя
"""
class LoginForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'password']
        widgets = {
            "password": forms.PasswordInput
        }

"""
    Регистрация переделана на стандартного пользователя
"""
class RegisterForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'patronym_name', 'phone', 'password']
        widgets = {
            "password": forms.PasswordInput
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user