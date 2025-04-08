from django.http import JsonResponse
from django.shortcuts import redirect

from functools import wraps

import jwt

from .models import CustomUser
from .utils import decode_jwt_token,is_token_blacklisted


# Декоратор нашей системы токенов на сайте
def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('jwt_token') # проверка наличия токена в куки  
        if not token:
            return redirect('login') # если гость попытается воспользоватся функционалом сайта его сразу перекинет на логин  
        try:
            if is_token_blacklisted(token): # проверка ,не тли токена в черном списке в редисе
                return JsonResponse({'error': 'Токен недействителен (черный список)'}, status=401)
            payload = decode_jwt_token(token)  # вытаскиваем данные с токена
            token_id = payload.get('id') 
            request.user = CustomUser.objects.get(id=token_id) # для дальнейшей работы с представлениями 
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Токен истек'}, status=401)
        except (jwt.InvalidTokenError, CustomUser.DoesNotExist):
            return JsonResponse({'error': 'Неверный токен'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view