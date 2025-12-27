from django.db import models

class Keyboard(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField()
    
    def __str__(self):
        return self.name
    
