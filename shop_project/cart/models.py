from django.conf import settings
from django.db import models


from shop.models import Product


# Create your models here.
class Cart(models.Model):
    cart_code = models.CharField(max_length=250, unique=True)
    paid_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    products= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)