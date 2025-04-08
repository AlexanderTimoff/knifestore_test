from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

import re


User = get_user_model()

# Здесь все валидации

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password','phone_number','password_confirm']
        labels = {  
            'username': 'Имя пользователя',  
            'email': 'Электронная почта', 
            'phone_number':'Номер телефона'   
        }
        help_texts = {
            'username': None,  
        }
       
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if len(username) > 15:
                raise ValidationError("Имя пользователя должно содержать 15 символов или меньше.")
            if not re.match(r'^[a-zA-Z0-9]+$', username):
                raise ValidationError("Имя пользователя может содержать только буквы и цифры.")
            if User.objects.filter(username=username).exists():
                raise ValidationError("Логин уже занят.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise ValidationError("Пароль должен содержать как буквы, так и цифры.")
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Электронная почта уже занята.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number') 
        phone_re= re.compile(r'^\+7\d{10}$')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Номер телефона уже занят.")
        if not phone_re.match(phone_number):
            raise forms.ValidationError("Номер телефона должен быть в формате: +77001234567.")
        return phone_number
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Пароли не совпадают.")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
