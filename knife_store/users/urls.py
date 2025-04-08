from django.urls import path
from .views import RegisterView, LoginView,LogoutView,PasswordResetCodeView,PasswordResetView,PasswordResetFormView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'), 
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),  # Страница ввода email для сброса пароля
    path('password_reset/code/', PasswordResetCodeView.as_view(), name='password_reset_code'),  # Страница для ввода кода
    path('password_reset/<str:email>/form/', PasswordResetFormView.as_view(), name='password_reset_form'),  # Страница для ввода нового пароля
]


