from django.conf.urls import url
from django.urls import path
from food import views

urlpatterns = [
    path('pizza',views.pizza_view, name='pizza'),
    path('pizza_price',views.pizza_price_view, name='pizza_price'),
    path('menu',views.menu_view, name = 'menu'),
    path('sub',views.sub_view, name = 'sub')

]