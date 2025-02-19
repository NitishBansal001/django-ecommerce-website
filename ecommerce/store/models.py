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
    image = models.ImageField( upload_to='pics/',blank=True,null=True)

    def __str__(self):
        return f'{self.name}'
    
    # for acessing it like an attribute
    @property
    def imageURL(self):
        try :
            url = self.image.url
        except:
            url = ''
        return url   


  
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)
   
    def __str__(self):
        return f'{self.transaction_id}'
    
    @property
    def get_cart_total(self):
        items = OrderItem.objects.filter(order=self)
        total = sum([item.get_total for item in items])
        return total
    
    @property
    def get_items_total(self):
        items = OrderItem.objects.filter(order=self)
        total= sum([item.quantity for item in items])
        return total

    @property
    def shipping(self):
    # Check if there are any non-digital products in the order
        return OrderItem.objects.filter(order=self, product__digital=False).exists()



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True )
    order = models.ForeignKey(Order,on_delete=models.SET_NULL ,null=True )
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product}------{self.order}'
    
    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL ,null=True )
    order = models.ForeignKey(Order,on_delete=models.SET_NULL ,null=True )
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    zipcode =  models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.address}'
    
