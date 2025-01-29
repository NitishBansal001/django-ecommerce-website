from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, redirect
# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html',{'products':products})

def cart(request,customer_id):
    cart = get_object_or_404(Customer,pk=customer_id,user=request.user)
    if request.method == 'POST':
        form=CustomerForm(request.POST,request.FILES)
        if form.is_valid():
            cart=form.save(commit=False)
            cart.user=request.user
            cart.save()
            return redirect('cart.html')
    else:
        form = CustomerForm()
    return render(request, 'cart.html',{'cart':cart})

def checkout(request):
    return render(request, 'checkout.html')
