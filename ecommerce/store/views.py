from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404,get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
import uuid
# Create your views here.


# def index(request):
#     products = Product.objects.all()
#     if request.user.is_authenticated:
#         currentorder = Order.objects.filter(customer__user=request.user, complete = False).first()
#     else :
#         currentorder = 
        
		
#     return render(request, 'index.html',{'products':products,'order':currentorder})
def index(request):
    products = Product.objects.all()
    
    if request.user.is_authenticated:
        # For authenticated users, fetch the incomplete order
        currentorder = Order.objects.filter(customer__user=request.user, complete=False).first()
    else:
        # For anonymous users, check if the 'order_id' cookie exists
        currentorder_id = request.COOKIES.get('currentorder_id')
        print('currentorder_id',currentorder_id)
        if currentorder_id:
            # If 'order_id' cookie exists, fetch the order
            currentorder = Order.objects.filter(id=currentorder_id, complete=False).first()
        else:
            # If no 'order_id' cookie, create a new order and set the cookie
            print('2currentorder_id',currentorder_id,shipping=False)
            currentorder = None


    # Render the template with the products and the current order
    response = render(request, 'index.html', {'products': products, 'order': currentorder})

    # If there's no current order, create a new order and store its ID in the cookie
    if not currentorder:
        new_order = Order.objects.create(complete=False)  # You may want to add other fields like user/customer
        response.set_cookie('currentorder_id', new_order.id, max_age=60*60*24*365)  # Cookie will last for 1 year

    return response


# def cart(request):
    
#     order = Order.objects.filter(customer__user=request.user,complete=False).first()
#     if not order:
#         orderitems = []
#     else :
#         orderitems = OrderItem.objects.filter(order=order)
#     return render(request, 'cart.html',{'orderitems':orderitems,'order':order})

def cart(request):
    # For authenticated users
    if request.user.is_authenticated:
        order = Order.objects.filter(customer__user=request.user, complete=False).first()
        
        if not order:
            orderitems = []
        else:
            orderitems = OrderItem.objects.filter(order=order)
    
    # For anonymous users (use session to manage cart)
    else:
        # Use a session variable for storing the cart items
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            currentOrder = Order.objects.filter(cart_id=cart_id, complete=False).first()
            if not currentOrder:
                currentOrder = Order.objects.create(cart_id=cart_id, complete=False)

        
        elif not cart_id:
            # Create a new empty order in the session if no cart_id exists
            order = None
            orderitems = []
            request.session['cart_id'] = str(request.session.session_key)  # or generate a unique identifier
        else:
            # Optionally, if cart_id exists, associate with a session-based order or create a new one
            order = Order.objects.filter(cart_id=cart_id, complete=False).first()
            if not order:
                order = Order(cart_id=cart_id, complete=False)
                order.save()

            orderitems = OrderItem.objects.filter(order=order)

    return render(request, 'cart.html', {'orderitems': orderitems, 'order': order})

def add_to_cart(request,product_id,action):
    print('Add_to_cart called')
    productsAll = Product.objects.all()
    currentOrder = Order.objects.filter(customer__user=request.user, complete = False).first()
    product = Product.objects.get(pk=product_id)

    existingIncompleteOrderItem = OrderItem.objects.filter(order__customer__user=request.user, order__complete = False, product=product).first()
    customer = Customer.objects.get(user=request.user)
    
    print('existingInncompleteOrder : ', existingIncompleteOrderItem)
    
    if action == 'add':
        if not existingIncompleteOrderItem: 
            print('to create new order')
            currentOrder = Order.objects.filter(customer__user=request.user, complete = False).first()
            if not currentOrder:
                currentOrder = Order.objects.create(
                    customer=customer,
                    complete=False,
                    transaction_id=uuid.uuid4()
                )
            orderitems = OrderItem.objects.create(
                product = product,
                order = currentOrder,
                quantity = 1
            )
            print('Order created successfoull going to cart.html')
        else:
            existingIncompleteOrderItem.quantity += 1
            existingIncompleteOrderItem.save()
            print('inside else of add case existingInncompleteOrder : ', existingIncompleteOrderItem.quantity)

    elif action == 'remove':
        if currentOrder:
            if existingIncompleteOrderItem and existingIncompleteOrderItem.quantity > 1:
                existingIncompleteOrderItem.quantity -= 1
                existingIncompleteOrderItem.save()
            elif existingIncompleteOrderItem :
                existingIncompleteOrderItem.delete()
            print('existingInncompleteOrder : ', existingIncompleteOrderItem)

    return render(request, 'index.html',{'products':productsAll,'order':currentOrder})


def checkout(request):
    order = get_object_or_404(Order,customer__user=request.user,complete=False)
    orderitems = get_list_or_404(OrderItem,order=order)
    print('order',order)
    print('orderitems',orderitems)
    if request.method == "POST":
        form = ShippingAddressForm(request.POST,request.FILES)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            print('saved',shipping_address.user)
            order.complete = True
            order.save()
            return redirect('index')
    else:
        form = ShippingAddressForm()

    return render(request, 'checkout.html',{'orderitems':orderitems,'order':order,'form':form})
