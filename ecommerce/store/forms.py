from django import forms
from .models import *


class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ("name",'email')

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ("name","price","image")

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ("customer","complete","transaction_id")

class OrderItemForm(forms.ModelForm):
    
    class Meta:
        model = OrderItem
        fields = ("product","order","quantity")

class ShippingAddressForm(forms.ModelForm):
    
    class Meta:
        model = ShippingAddress
        fields = ("address","city","state","zipcode")



