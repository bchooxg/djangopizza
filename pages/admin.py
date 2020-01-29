from django.contrib import admin

# Register your models here.
from .models import User_Profile, Cart, Cart_Item, Order, Order_item, Order_Status

# Adding the table to the admin interface
admin.site.register(User_Profile)

# class Cart_Admin(admin.ModelAdmin):
#     readonly_fields = ('id',)

admin.site.register(Cart)
admin.site.register(Cart_Item)

admin.site.register(Order)
admin.site.register(Order_item)
admin.site.register(Order_Status)





