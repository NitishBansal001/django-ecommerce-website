from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ShippingAddressForm(forms.ModelForm):
    
    class Meta:
        model = ShippingAddress
        fields = ('address','city','state','zipcode')



class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email','password1','password2')


        