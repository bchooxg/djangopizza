from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from .models import User_Profile, Cart, Order
from food import models
import stripe
from decimal import Decimal


# Create your views here.
def index_view(request):
    return render(request, 'index.html')

def order_view(request,id):        
    order = Order.objects.get(id=id)
    if order.cust_id == request.user or request.user.is_staff:
        items = order.order_items.all()
        total = 0
        for item in items :
            total += item.price
        

        return render(request,"order_details.html",{"order":order, "total":total})
    else:
        messages.error(request,"You are not authorized to view that order")
        return redirect('index')

def user_view(request):

    try :
        user = User.objects.get(username = request.user)
    except:
        messages.error(request, "Please Login To add to cart")
        return redirect('menu')
    
    orders = Order.objects.filter(cust_id = user.id).all()

    return render(request,'user.html', {"orders":orders})

##################################### CheckOut VIEWS ##################################

def checkout(request):
    if request.method == "POST":
        try :
            user = User.objects.get(username = request.user)
        except:
            messages.error(request, "Please Login To add to cart")
            return redirect('menu')


        pub_key = 'pk_live_Be5KKmQyeTKfJMoZCydE0OEd00TGJ3AHAA'
        secret_key = 'sk_live_fbFsoew1CcZULtMuRSX0VEi700AXjxO7i6'

        stripe.api_key = 'sk_test_JxeyPmXFFttXt9qLZLFj8W7g00udKbr6MH'
        amt = request.POST['cart_amt'] * 100

        


        # charge = stripe.Charge.create(
        # amount=amt,
        # currency='usd',
        # source='tok_visa',
        # receipt_email='jenny.rosen@example.com',
        # )
        # Get The cart
        cart = Cart.objects.get(user_id = user.id)
        # Get cart objects
        cart_items = cart.cart_items.all()
        # Create Order
        order = Order.objects.create(cust_id = user)
        #  Move cart items to order items
        for item in cart_items:
            order.order_items.create(order_id = order.id, description=item.description, size=item.size , qty=item.qty, toppings=item.toppings, price=item.price)
        # Assign Status 
        order.order_status.create(order_id = order.id, status = "Created")
        # delete cart
        cart.delete()
        return redirect('user_view')

##################################### STAFF VIEWS ##################################

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def staff_view(request):
    if request.method == "POST":
        order_id = request.POST['order']
        order = Order.objects.get(pk=order_id)

        if order.order_status.latest().status == "Created":        
            order.order_status.create(order_id = order.id, status = "Accepted")
            return redirect('staff_view')


        if order.order_status.latest().status == "Accepted":
            order.order_status.create(order_id = order.id, status = "Preparing Food")
            return redirect('staff_view')


        if order.order_status.latest().status == "Preparing Food":
            order.order_status.create(order_id = order.id, status = "Out For Delivery")
            return redirect('staff_view')


        if order.order_status.latest().status == "Out For Delivery":
            order.order_status.create(order_id = order.id, status = "Completed")
            return redirect('staff_view')





    orders = Order.objects.all()
    context = {"orders": orders}
    return render(request, 'staff_view.html', context)

################################### CART ###########################################

# This function is used to check if the item is already in cart
def cartcheck(model, description, price, cart_id, size="", toppings=""):
    try :
        a = model.cart_items.get(description = description, size=size, toppings=toppings)
    except:
        a = None
    if a != None:
        a.qty += 1 
        a.price += price
        a.save()
    else:
        model.cart_items.create(cart_id=cart_id, description=description, price=price, size=size, toppings=toppings)


def add_to_cart_view(request, id):

     
    try :
        user = User.objects.get(username = request.user)
    except:
        messages.error(request, "Please Login To add to cart")
        return redirect('menu')

    if request.user.cart.exists():

        # Add cart item to their cart
        cart = Cart.objects.get(user_id = user.id)
        # Get item information and add it to cart
        item = models.Menu_Item.objects.get(pk=id)
        # cart.cart_items.create(cart_id = cart.id, description = item.item_name, price = item.item_price)
        cartcheck(cart_id = cart.id, model = cart, description = item.item_name, price=item.item_price)
        messages.success(request, f"{item.item_name} added to cart!")
        return redirect('menu')
        # TO DO 
        # CREATE Cart Page
        # Create seperate add to cart for pizza 
    else:

        # If user dosent have a cart, creates one for them
        Cart.objects.create(user_id = user)
        # Get item information and add it to cart
        cart = Cart.objects.get(user_id = user.id)
        item = models.Menu_Item.objects.get(pk=id)
        # cart.cart_items.create(cart_id = cart.id, description = item.item_name, price = item.item_price)
        cartcheck(cart_id = cart.id, model = cart, description = item.item_name, price=item.item_price)
        messages.success(request, f"{item.item_name} added to cart!")
        return redirect('menu')
    pass

def pizza_add_to_cart_view(request):
    try :
        user = User.objects.get(username = request.user)
    except:
        messages.error(request, "Please Login To add to cart")
        return redirect('pizza')

    pizza_size = request.POST['pizza_size']
    pizza_type = request.POST['pizza_type']
    topping = request.POST.getlist('topping')

    
    if request.user.cart.exists():
        cart = Cart.objects.get(user_id = user.id)
        pizza = models.Pizza.objects.get(pizza_size = pizza_size, pizza_type=pizza_type, topping_count= len(topping)+1)
        # cart.cart_items.create(cart_id = cart.id, size = pizza.pizza_size, description = pizza, price = pizza.item_price, toppings = topping)
        cartcheck(cart_id = cart.id, model = cart, size=pizza.pizza_size, description = pizza, price=pizza.item_price, toppings = topping)

        messages.success(request, f"Pizza added to cart!")
        return redirect('pizza')

    else:

        # If user dosent have a cart, creates one for them
        Cart.objects.create(user_id = user)
        # Get item information and add it to cart
        cart = Cart.objects.get(user_id = user.id)
        pizza = models.Pizza.objects.get(pizza_size = pizza_size, pizza_type=pizza_type, topping_count= len(topping)+1)
        # cart.cart_items.create(cart_id = cart.id, size = pizza.pizza_size, description = pizza, price = pizza.item_price, toppings = topping)
        cartcheck(cart_id = cart.id, model = cart, size=pizza.pizza_size, description = pizza, price=pizza.item_price, toppings = topping)
        messages.success(request, f"Pizza added to cart!")
        return redirect('pizza')
    pass

def sub_add_to_cart_view(request):
    if request.method == "POST":
        try :
            user = User.objects.get(username = request.user)
        except:
            messages.error(request, "Please Login To add to cart")
            return redirect('sub')
        
        sub_id = request.POST['sub_id']
        sub = models.Sub.objects.get(pk=sub_id)

        if request.POST['size'] == "small":
            sub_size = "Small"
            sub_price = sub.small_price
            sub_name = "Small" + sub.item_name + "Sub"
        if request.POST['size'] == "large":
            sub_size = "Large"
            sub_price = sub.large_price
            sub_name = "Large " + sub.item_name + " Sub"


        toppings = request.POST.getlist('toppings')

        topping_price = Decimal(len(toppings)*0.5)

        final_price = sub_price + topping_price

        if request.user.cart.exists():
            cart = Cart.objects.get(user_id = user.id)
            cartcheck(cart_id = cart.id, model = cart, size=sub_size, description = sub_name, price=final_price, toppings = toppings)
            messages.success(request, f"Sub added to cart!")
            return redirect('sub')

        else:
            # If user dosent have a cart, creates one for them
            Cart.objects.create(user_id = user)
            # Get item information and add it to cart
            cart = Cart.objects.get(user_id = user.id)
            cartcheck(cart_id = cart.id, model = cart, size=sub_size, description = sub_name, price=final_price, toppings = toppings)
            messages.success(request, f"Sub added to cart!")
            return redirect('sub')


        


    else:
        messages.error(request,"Unauthorized Method")
        return redirect('index')

def remove_frm_cart_view(request,id):
    try :
        user = User.objects.get(username = request.user)
    except:
        messages.error(request, "Please Login To add to cart")
        return redirect('index')

    cart = Cart.objects.get(user_id = user)

    try:
        a = cart.cart_items.get(id=id)
    except:
        a = None
    
    if a == None :
        messages.error(request, "Unable to find item in your cart")
        return redirect('cart')
    else:
        a.delete() 
        messages.success(request,"Item has been removed from cart")
        return redirect('cart')




def cart_view(request):

    try :
        user = User.objects.get(username = request.user)
    except:
        messages.error(request, "Please Login To add to cart")
        return redirect('menu')

    try:
        cart = Cart.objects.get(user_id = user)
        cart_items = cart.cart_items.all()
        cart_total = 0
        for item in cart_items:
            cart_total += item.price
            
        return render(request,"cart.html", {'cart_items':cart_items, 'cart_total':cart_total})
    except:
        return render(request,"cart.html")


############################### USER LOGIN ###########################################################
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user != None :
            auth.login(request,user)
            messages.info(request,"You Have Been Logged In")
            return redirect('index')
        else:
            messages.error(request,"Invalid Credentials, Please Try Again")
            return redirect('login')
    else:
        return render(request,'login.html')

def logout_view(request):
    auth.logout(request)
    messages.info(request,"You have been logged out, See you soon!")
    return redirect('index')

def signup_view(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = auth.authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            auth.login(request, new_user)
            return redirect('index')
    else:
        form = UserCreationForm
        # CREATE A INSTANCE OF PROFILE FORM TO BE ADDED
    return render(request,'signup.html', {"form": form})
