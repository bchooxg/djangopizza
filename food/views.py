from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse

from food import models

def menu_view(request):
    menu = models.Menu_Item.objects.all().exclude(category = 4 ) # Excludes items that are subs
    return render(request,'menu.html', {"menu":menu})

def sub_view(request):
    subs = models.Sub.objects.all()
    toppings = models.Sub_Topping.objects.all()
    return render(request,'sub.html',{"subs":subs,"toppings":toppings})


# Create your views here.
def pizza_view(request):
    # need to query the database and get the correct ingredients
    types = models.Pizza_Type.objects.all()
    toppings = models.Topping.objects.all()
    sizes = models.Size.objects.filter(size='Small') | models.Size.objects.filter(size='Large')

    context = {'types': types, 'toppings':toppings, 'sizes':sizes}
    return render(request,'pizza.html', context)

# API that returns a json object containing the price of the pizza
def pizza_price_view(request):
    pizza_size = request.GET.get('pizza_size', None)
    pizza_type = request.GET.get('pizza_type', None)
    topping_count = request.GET.get('topping_count', None)
    price = (models.Pizza.objects.filter(pizza_size=pizza_size, pizza_type=pizza_type, topping_count=topping_count ).get()).item_price
    data = {
        'price': price
    }
    return JsonResponse(data)