from django.shortcuts import render
from django.utils import timezone

from users.decorators import token_required
from products.models import Product 


@token_required
def user_cabinet(request):
    user = request.user
    user_ads = Product.objects.filter(user=user)
    for product in user_ads:
        if product.ad_type == 'top' and product.ad_expiration and product.ad_expiration > timezone.now():
            product.ad_status = f"Топ-реклама, будет вверху до {product.ad_expiration.strftime('%d-%m-%Y')}"
        elif product.ad_type == 'highlight' and product.ad_expiration and product.ad_expiration > timezone.now():
            product.ad_status = f"Выделено рамкой до {product.ad_expiration.strftime('%d-%m-%Y')}"
        elif product.ad_type == 'special' and product.ad_expiration and product.ad_expiration > timezone.now():
            product.ad_status = f"В спецблоке до {product.ad_expiration.strftime('%d-%m-%Y')}"

    return render(request, 'cabinet/cabinet.html', {'user': user, 'user_ads': user_ads})
