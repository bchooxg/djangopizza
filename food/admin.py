from django.contrib import admin

# Register your models here.
from .models import Topping, Menu_Item, Category, Size, Sub, Sub_Topping, Pizza, Pizza_Type, Topping_Count


admin.site.register(Menu_Item)
admin.site.register(Category)
admin.site.register(Sub)
admin.site.register(Sub_Topping)
admin.site.register(Pizza)
admin.site.register(Topping)

class Pizza_Type_Admin(admin.ModelAdmin):
    readonly_fields = ('id',)


class Size_Admin(admin.ModelAdmin):
    readonly_fields = ('id',)

class Topping_Count_Admin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Pizza_Type, Pizza_Type_Admin)
admin.site.register(Size, Size_Admin)
admin.site.register(Topping_Count, Topping_Count_Admin)
