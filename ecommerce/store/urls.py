from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    
    path('add_to_cart/<int:product_id>/<str:action>/',views.add_to_cart,name="add_to_cart"),
]
