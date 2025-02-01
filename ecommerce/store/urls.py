from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('search_bar/',views.search_bar,name='search_bar'),
    path('add_to_cart/<int:product_id>/<str:action>/',views.add_to_cart,name="add_to_cart"),
    path('register',views.register,name="register"),
]
