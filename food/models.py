from django.db import models
from django.contrib import admin

# Create your models here.

# Size Model to show the different sizes offered
class Size(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.size  

class Menu_Item(models.Model):
    item_name = models.CharField(max_length=50)
    item_size = models.ForeignKey("Size", on_delete=models.CASCADE,)
    item_price = models.DecimalField(max_digits=100, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    images = models.ImageField(upload_to='menu_item_photos', null=True)

    def __str__(self):
        return self.item_name  

  

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# SUB MODELS

class Sub(models.Model):
    # sizes = [
    #     ("Small", 'Small'),
    #     ("Large", 'Large')
    # ]
    item_name = models.CharField(max_length=50)
    # item_size = models.CharField(choices=sizes,max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=4)
    small_price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    large_price = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    images = models.ImageField(upload_to='menu_item_photos', null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} Sub"

class Sub_Topping(models.Model):
    description = models.CharField(max_length=50)
    topping_price = models.DecimalField(max_digits=100, decimal_places=2)
    def __str__(self):
        return self.description  



# PIZZA MODELS

class Pizza(models.Model):
    pizza_type = models.ForeignKey('Pizza_Type', on_delete=models.CASCADE)
    pizza_size = models.ForeignKey("Size", on_delete=models.CASCADE, null=True)    
    topping_count = models.ForeignKey('Topping_Count', on_delete=models.CASCADE)
    item_price = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return f"[{self.pizza_type}] [{self.pizza_size}] [{self.topping_count}] [${self.item_price}]"

class Pizza_Type(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description 

class Topping_Count(models.Model):
    amt = models.IntegerField()
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description 



# Standalone Table 

class Topping(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description  



