from django.shortcuts import render
from django.views import View
from users.utils import decode_jwt_token
from products.models import Product
from django.utils.timezone import now

class HomeView(View):
    def get(self, request):
        # Получение всех автомобилей
        products = Product.objects.all()
        # Фильтрация автомобилей по типу рекламы
        highlighted_ads = Product.objects.filter(ad_type='highlight', ad_expiration__gt=now())
        top_ads = Product.objects.filter(ad_type='top', ad_expiration__gt=now()).order_by('-added_to_top_at') 
        # Фильтрация для темплейтов , потом используется чтоб правильно отображались рекламные и не рекламные обьявления
        for product in products:
            product.is_highlighted = product in highlighted_ads
        for product in products:
            product.is_top = product in top_ads
        context = {
            'highlighted_ads': highlighted_ads,
            'top_ads': top_ads,
            'products': products,  
        }
       
        # Проверка аутентификации через токен,для не вошедших пользователей другая информация
        token = request.COOKIES.get('jwt_token')
        # флажок для темплейта
        is_authenticated = False
        if token:
            try:
                user_id = decode_jwt_token(token)
                if user_id:
                    is_authenticated = True
            except Exception as e:
                print(f'Ошибка декодирования токена: {e}')
        context['is_authenticated'] = is_authenticated
        return render(request, 'base.html', context)

# отображение странички разработчик (моей)
class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')
