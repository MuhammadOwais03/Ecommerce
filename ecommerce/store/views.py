from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from .form import NewUserRegistration




def registration_form(request):
    if request.method == "POST":
        form = NewUserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            customer = Customer(user=user, name=user.username, email=user.email)
            customer.save()
            login(request,user)
            messages.success(request, f'{user.username} Have Successfully Register')
            return redirect('store')
        else:
            messages.error(request, "Invalid")
    
    form = NewUserRegistration()
    return render(request, 'registration/register.html', {"register_form":form})


def login_view(request):
    next = request.GET.get("next")
    if next:
        messages.error(request, "You Need To Login")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"{username} has successfully login")
                return redirect("store")
            else:
                messages.error(request, "Invalid Username Or Password")
        else:
               messages.error(request, "Invalid Username Or Password")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {"login_form":form})
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')

# Create your views here.

def store(request):
    product = Product.objects.all()
    
    if request.user.is_authenticated:
        customer = request.user.customer
        cus = Customer.objects.get(name=customer)
        if Order.objects.filter(customer=customer).exists():
            order_id = Order.objects.get(customer=customer).id
            orderitems = len(OrderedItem.objects.filter(order=order_id))
            content = {"product":product, 'count':orderitems, "customer":customer}
            return render(request, 'store/store.html', content)
        
    content = {"product":product}
    return render(request, 'store/store.html', content)



@login_required
def cart(request):
    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            customer_id = Customer.objects.get(name=customer).id
            order, created = Order.objects.get_or_create(customer=customer)
            items = OrderedItem.objects.filter(order=order)
            order.totalPrice = 0
            for item in items:
                item.total = item.product.price * item.quantity
                OrderedItem.objects.filter(product_id=item.product).update(total=item.total)
                order.totalPrice += item.total
            order.save()
        context = {"items":items, "order_totalPrice":order.totalPrice, "length":len(items), 'id':customer_id, "order_id":order}
        return render(request, 'store/cart.html', context)
    except Exception as e:
        print(e)
        return render(request, 'store/cart.html', {"display":True})

def delete(request, id):
    item = OrderedItem.objects.filter(id=id)
    item.delete()
    return redirect('cart')



def checkout(request, order_id=None, customer_id=None):
    if ShippingAddress.objects.filter(customer_id=customer_id).exists():
        customer = Customer.objects.get(id=customer_id)
        items = OrderedItem.objects.filter(order=order_id)
        shipping_information = ShippingAddress.objects.get(customer_id=customer_id)
        context = {"items":items, "shipping_information": shipping_information, "customer":customer, "customer_id":customer_id, 'order_id':order_id}
        return render(request, 'store/checkout.html', context)
    else:
        items = OrderedItem.objects.filter(order=order_id)
        customer = Customer.objects.get(id=customer_id)
        context = {"items":items, "display":True, "customer":customer, "customer_id":customer_id, 'order_id':order_id}
        return render(request, 'store/checkout.html', context)
@login_required
def addTocart(request, id):
    
        if request.user.is_authenticated:
            customer = request.user.customer
            cus = Customer.objects.get(name= customer).id
            print(cus)
            order, created = Order.objects.get_or_create(customer_id=cus)
            order_id = Order.objects.get(customer=cus).id
            if not(OrderedItem.objects.filter(order=order_id, product_id=id).exists()):
                orderitem = OrderedItem.objects.create(product_id=id, order=order, quantity=+1)
                count = len(OrderedItem.objects.filter(order=order))
                return redirect("store")
            else:
                o =OrderedItem.objects.filter(order_id=order_id,product_id=id).get()
                o.quantity += 1 
                orderitem=OrderedItem.objects.filter(order_id=order_id, product_id = id).update(quantity=o.quantity)
                count = len(OrderedItem.objects.filter(order=order))
                return redirect("store") 

def increase_count(request, order_id, product_id):

    o =OrderedItem.objects.filter(order_id=order_id,product_id=product_id).get()
    o.quantity += 1 
    orderitem=OrderedItem.objects.filter(order_id=order_id, product_id = product_id).update(quantity=o.quantity)
    return redirect('cart')
def decrease_count(request, order_id, product_id):

    o =OrderedItem.objects.filter(order_id=order_id,product_id=product_id).get()
    o.quantity -= 1 
    orderitem=OrderedItem.objects.filter(order_id=order_id, product_id = product_id).update(quantity=o.quantity)
    return redirect('cart')


def checkoutform(request, cus_id, ord_id):
    
    if request.method == "POST":
        print(request.POST)
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip = request.POST.get("zip")
        
        if ShippingAddress.objects.filter(customer_id=cus_id).exists():
            ShippingAddress.objects.filter(customer_id=cus_id).update(city=city, state=state, zipcode=zip, address=address)
        else:
            ShippingAddress.objects.create(customer_id=cus_id, order_id=ord_id, city=city, state=state, zipcode=zip, address=address)
        
        

        print(request.POST)
    return redirect('checkout', order_id = ord_id, customer_id=cus_id)

