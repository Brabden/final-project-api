from django.db import models
from django.contrib.auth.models import User
from products.models import Keyboard

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self):
        return f"Cart for {self.user or 'Guest'}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Keyboard, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def get_total_price(self):
        return self.quantity * self.product.price
