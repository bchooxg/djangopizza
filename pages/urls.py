from django.conf.urls import url
from django.urls import path
from pages import views

urlpatterns = [
    url(r'^$',views.index_view, name='index'),
    url(r'^signup',views.signup_view, name='signup'),
    path('add_to_cart/<int:id>',views.add_to_cart_view, name='add_to_cart'),
    path('pizza_add_to_cart',views.pizza_add_to_cart_view, name='pizza_add_to_cart'),
    path('sub_add_to_cart',views.sub_add_to_cart_view, name='sub_add_to_cart'),
    path('remove_frm_cart/<int:id>', views.remove_frm_cart_view, name="remove_frm_cart"),
    path('cart',views.cart_view, name='cart'),
    path('order/<int:id>',views.order_view, name='order'),
    path('staff_view',views.staff_view, name='staff_view'),
    path('user',views.user_view, name='user_view'),
    path('checkout',views.checkout,name='checkout'),
    url(r'^login',views.login_view, name='login'),
    url(r'^logout',views.logout_view, name='logout')

]