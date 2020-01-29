from django.db import models
from django.contrib.auth.models import User
from food.models import Menu_Item, Pizza

# Create your models here.
class User_Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    # username = models.CharField(max_length=50)
    # password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    unit_number = models.CharField(max_length=50,blank=True)
    postal_code = models.DecimalField(max_digits=6,decimal_places=0,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE, null=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    # cart_items = models.ManyToManyField("Cart_Items")
    # menu_items = models.ManyToManyField(Menu_Item)
    # pizzas = models.ManyToManyField(Pizza)


    def __str__(self):
        return str(self.user_id) + "'s Cart"

class Cart_Item(models.Model):
    cart_id = models.ForeignKey("Cart", related_name="cart_items",  on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    size = models.CharField(max_length=50, blank=True)
    toppings = models.CharField(max_length=50, blank=True)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6,decimal_places=2,null=True)

    def __str__(self):
        return str(self.description)

class Order(models.Model):
    cust_id = models.ForeignKey(User, related_name="order",on_delete=models.CASCADE)


    def __str__(self):
        return str(f"Order ID:{self.id}      Customer: {self.cust_id}")

class Order_Status(models.Model):

    STATUS_CHOICES = [
        ("Created", 'Created'),
        ("Payment Declined", 'Payment Declined'),
        ("Accepted", 'Accepted'),
        ("Preparing Food", 'Preparing Food'),
        ("Out For Delivery", 'Out For Delivery'),
        ("Completed", 'Completed')
    ]
    order_id = models.ForeignKey("Order", related_name="order_status",on_delete=models.CASCADE)
    status = models.CharField( max_length=50, choices=STATUS_CHOICES,)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        get_latest_by = ['id']

    def __str__(self):
        return self.status

class Order_item(models.Model):
    order_id = models.ForeignKey("Order", related_name="order_items",  on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    size = models.CharField(max_length=50, blank=True)
    toppings = models.CharField(max_length=50, blank=True)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6,decimal_places=2,null=True)

    def __str__(self):
        return str(self.description)

