from django.contrib import admin
from .models import Product, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'clas', 'year', 'price', 'user', 'created_at', 'ad_paid')
    list_filter = ('brand', 'clas', 'year', 'ad_paid')
    search_fields = ('brand', 'clas', 'description')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')