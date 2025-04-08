from django import forms

from .models import Product,ProductImage
from .constant import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
                  'brand', 
                  'clas', 
                  'year',  
                  'description',  
                  'price', 
                  'additional_phone']
        labels = {
            'brand': 'Название ',
            'clas': 'Редкость',
            'year': 'Год выпуска',
            'description': 'Описание',
            'price': 'Цена (KZT)',
            'additional_phone': 'Телефон'
        }
         
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        labels = {'image':'Фото'}
    
    def clean_image(self):
        images = self.cleaned_data.get('image')
        if not images.name.endswith(('.png', '.jpg', '.jpeg','.jfif','.webp')):
                raise forms.ValidationError('Формат не поддерживается. Разрешенные форматы: .png, .jpg, .jpeg, .jfif, .webp')
        return images
    
ProductImageFormSet = forms.modelformset_factory(ProductImage, form=ProductImageForm, extra=5)
    
class AdTypeForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['ad_type']
   
    
    
    
    
    
    
    
    