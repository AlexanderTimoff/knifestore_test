from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm

import datetime
import random
import string

from .models import CustomUser 
from .forms import RegistrationForm, LoginForm
from .utils import create_jwt_token,decode_jwt_token,blacklist_token

# Определяем кастомного юсера с сеттингс
User = get_user_model()

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'users/registr.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()
            return redirect('login')  # Переход на страницу логина после успешной регистрации
        return render(request, 'users/registr.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                if user.check_password(password): # Проверка пароля 
                    token = create_jwt_token(user) # Присвоение токена в случае если пароль правильный
                    print(type(token))
                    response = JsonResponse({'success': True, 'token':  token}) 
                    response.set_cookie('jwt_token', token, httponly=True, secure=True) # Передаем токен в куки с исползованием протоколов безопасности 
                    return response
                else:
                    return JsonResponse({'success': False, 'error': 'Неправильное имя пользователя или пароль'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Неправильное имя пользователя или пароль'}, status=400)    
        else:
            return JsonResponse({'errors': form.errors}, status=400)

class LogoutView(View):
    def post(self, request):
        token = request.COOKIES.get('jwt_token') # при выходе пользователя берем его токен  
        if token:
            try:
                payload = decode_jwt_token(token) # декодируем токен 
                exp = payload.get('exp') # вытаскиваем время истечения токена 
                exp = int(exp)
                expiration_time = datetime.datetime.fromtimestamp(exp, tz=datetime.timezone.utc) # приводим к одному формату времени
                current_time = datetime.datetime.now(datetime.timezone.utc)
                ttl = (expiration_time - current_time).total_seconds() 
                ttl=int(ttl)
                blacklist_token(token, ttl) # отправляем в черный список в редис,токен удалится когда истечет ттл который совпадет с истечением времени самого токена 
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Токен отсутствует.'}, status=400)
        response = redirect('/')  
        response.delete_cookie('jwt_token')  # удаляем токен с куки после выхода
        return response
    

#Система восстановения пароля через почту ,страница для ввода почты и отправки кода
class PasswordResetView(View):
    def get(self, request):
        return render(request, 'users/password_reset.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email) # Проверка есть ли пользователь с такой почтой в нашей базе данных
            # Генерация случайного кода
            reset_code = ''.join(random.choices(string.ascii_uppercase, k=4))
            user.reset_code = reset_code  
            user.save()
            # Отправка кода на email
            send_mail(
                'Knife Store Сброс пароля',
                f'Здравствуйте,Ваш код для сброса пароля на сайте Knife Store: {reset_code}',
                'no-reply@example.com',
                [email],
            )
            return redirect(f'{reverse("password_reset_code")}?email={email}')  # Переход к вводу кода
        except CustomUser.DoesNotExist:
            return render(request, 'users/password_reset.html', {'error': 'Пользователь с таким email не найден'})

# Система восстановления пароля страничка для ввода кода с почты
class PasswordResetCodeView(View):
    def get(self, request):
        email = request.GET.get('email')  # Получаем email через GET
        return render(request, 'users/password_reset_code.html', {'email': email})

    def post(self, request):
        email = request.GET.get('email')  
        reset_code = request.POST.get('code') 
        try:
            user = CustomUser.objects.get(email=email)
            if user.reset_code == reset_code: # Проверка введенного кода и кода с почты
                # Код верный, показываем форму для смены пароля
                return redirect('password_reset_form', email=email)
            else:
                return render(request, 'users/password_reset_code.html', {'error': 'Неверный код', 'email': email})
        except CustomUser.DoesNotExist:
            return render(request, 'users/password_reset_code.html', {'error': 'Пользователь с таким email не найден', 'email': email})

# Система восстановления пароля страничка для ввода нового пароля
class PasswordResetFormView(View):
    def get(self, request, email):
        try:
            # Получаем пользователя по email
            user = CustomUser.objects.get(email=email)
            # Создаем форму для смены пароля с использованием втроенного джанго метода  SetPasswordForm
            form = SetPasswordForm(user)
            return render(request, 'users/password_reset_form.html', {'form': form, 'email': email})
        except CustomUser.DoesNotExist:
            # Если пользователя нет, редиректим на страницу сброса пароля
            return redirect('password_reset')  

    def post(self, request, email):
        try:
            # Получаем пользователя по email
            user = CustomUser.objects.get(email=email)
            # Создаем форму с POST данными
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                # Сохраняем новый пароль
                form.save()
                # Перенаправляем на страницу логина после успешной смены пароля
                return redirect('login')
            return render(request, 'users/password_reset_form.html', {'form': form, 'email': email})
        except CustomUser.DoesNotExist:
            # Если пользователя с таким email нет
            return render(request, 'users/password_reset_form.html', {'error': 'Пользователь с таким email не найден', 'email': email, 'form': form})
