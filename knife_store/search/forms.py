from django import forms
from products.models import Product
from products.constant import *

class ProductSearchForm(forms.Form):
    brand = forms.ChoiceField(choices=[('', 'Выберите модель')] +Product._meta.get_field('brand').choices, required=False, label='Модель')
    clas = forms.ChoiceField(choices=[('', 'Выберите редкость')] +Product._meta.get_field('clas').choices, required=False, label='Редкость')
    year = forms.IntegerField(required=False, label='Год')
    price_min = forms.DecimalField(required=False, label='Минимальная цена', decimal_places=0)
    price_max = forms.DecimalField(required=False, label='Максимальная цена', decimal_places=0)
   