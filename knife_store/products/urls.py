from django.urls import path

from .views import create_product,edit_ad,delete_ad,detail_ad,promote_ad

urlpatterns = [
    path('create_product/', create_product, name='create_product'),
    path('ad/<int:product_id>/edit/', edit_ad, name='edit_ad'),
    path('ad/<int:product_id>/delete/', delete_ad, name='delete_ad'),
    path('product/<int:product_id>/', detail_ad, name='detail_ad'),
    path('promote/<int:product_id>/', promote_ad, name='promote_ad'),
    
]