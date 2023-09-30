from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    price = models.FloatField(null=True)
    
    image = models.ImageField(default='default_image.jpg')


    def __str__(self):
        return self.name

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    totalPrice = models.FloatField(default=0, null=True)
    date_ordered = models.DateTimeField(blank=False,auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True)


    def __str__(self):
        return str(self.id)
    
class OrderedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    total = models.FloatField(default=0, null=True)
    date_added = models.DateTimeField(null=True, blank=False, auto_now_add=True)

    def __str__(self):
        return str(self.id)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=200, blank=False)
    zipcode = models.CharField(max_length=200, blank=False)
    address = models.CharField(max_length=200, null=True, blank=False)
    date_added = models.DateTimeField(null=True, blank=False, auto_now_add=True)


   
