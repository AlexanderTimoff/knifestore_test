from django.db import models
from django.utils import timezone

from users.models import CustomUser
from .constant import *


def user_directory_path(instance, filename):
    return f'user_{instance.product.user.id}/product_images/{filename}'

class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    brand = models.CharField(max_length=50,choices=BRAND_CHOICES)
    clas = models.CharField(max_length=50,choices=CLAS_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    phone = models.BooleanField(default=False)  
    additional_phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ad_type = models.CharField(max_length=20, choices=AD_TYPE_CHOICES, default='none')
    ad_expiration = models.DateTimeField(null=True, blank=True) 
    ad_paid = models.BooleanField(default=False) 
    added_to_top_at = models.DateTimeField(null=True, blank=True) 
    is_highlighted = models.BooleanField(default=False)
    
    def is_ad_active(self):
        return self.ad_expiration and self.ad_expiration > timezone.now()
    def __str__(self):
        return f"{self.brand} {self.clas} ({self.year}) {self.id}"
       
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.brand} {self.product.clas}"
