from django.shortcuts import render, redirect,get_object_or_404
from django.utils import timezone

from datetime import timedelta

from .forms import ProductForm,ProductImageFormSet,AdTypeForm
from .models import Product, ProductImage
from users.decorators import token_required


@token_required
def create_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        image_formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if product_form.is_valid() and image_formset.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            for form in image_formset.cleaned_data:
                if form:
                    image = form['image']
                    ProductImage.objects.create(product=product, image=image)
            return redirect('user_cabinet') 
    else:
        product_form = ProductForm()
        image_formset = ProductImageFormSet(queryset=ProductImage.objects.none())
    return render(request, 'products/create_product.html', {'product_form': product_form, 'image_formset': image_formset})

# Редактирование обьявлений                
def edit_ad(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('user_cabinet') 
    else:
        product_form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'product_form': product_form})

# Удаление обьявлений                
def delete_ad(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('user_cabinet')  
    return render(request, 'products/delete_product.html', {'product': product})

# Для страницы с обьявлением               
def detail_ad(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()
    seller = product.user 
    return render(request, 'products/detail_ad.html', {
        'product': product,
        'images': images,
        'seller': seller,
    })
    
# Для выбора рекламы               
def promote_ad(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    error_message = " "  # Инициализация переменной для сообщения об ошибке
    if request.method == 'POST':
        form = AdTypeForm(request.POST, instance=product)
        if form.is_valid():
            ad_type = form.cleaned_data['ad_type']
            product.ad_type = ad_type 
            if ad_type == 'top':
                product.added_to_top_at = timezone.now()
            if ad_type != 'none':
                product.ad_expiration = timezone.now() + timedelta(days=1) 
            else:
                product.ad_expiration = None
            product.save()
            # Если выбрана реклама, отправляем на страницу оплаты
            if ad_type != 'none':
                return redirect('select_card_payment', product_id=product.id, ad_type=ad_type)
            else:
                error_message = 'Реклама отключена'       
    else:
        form = AdTypeForm(instance=product)
    return render(request, 'products/promote_ad.html', {'form': form, 'product': product, 'error_message': error_message})

