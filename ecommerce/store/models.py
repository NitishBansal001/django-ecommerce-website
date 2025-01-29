from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name}'
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField( upload_to='pics/', height_field=None, width_field=None, max_length=None,blank=True,null=True)

    def __str__(self):
        return f'{self.name}'
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return f'{self.transaction_id}'

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True )
    order = models.ForeignKey(Order,on_delete=models.SET_NULL ,null=True )
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL ,null=True )
    order = models.ForeignKey(Order,on_delete=models.SET_NULL ,null=True )
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    zipcode = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.address}'
    