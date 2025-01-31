from django import forms
from .models import *

class ShippingAddressForm(forms.ModelForm):
    
    class Meta:
        model = ShippingAddress
        fields = ('address','city','state','zipcode')
