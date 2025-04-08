from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.timezone import now

import random

from users.decorators import token_required
from .models import Card,Payment
from products.models import Product
from .forms import CardForm
from datetime import timedelta
from products.constant import AD_TYPE_PRICES
from decimal import Decimal


# Добавление платежной карты
@token_required
def add_card(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card_number = "".join([str(random.randint(0, 9)) for _ in range(16)])
            Card.objects.create(
                user=request.user,
                card_number=card_number,
                bank=form.cleaned_data['bank']
            )
            return redirect("card_list") 
    else:
        form = CardForm()
    return render(request, "payments/add_card.html", {"form": form})

# Удаление платежной карты
@token_required
def delete_card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    if request.user == card.user:
        card.delete() 
        return redirect('card_list')  
    else:
        return redirect('home')
    

# Пополнение платежной карты(бесконечные деньги)
@token_required
def recharge_balance(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        recharge_amount = request.POST.get('amount')
        if not card_id or not recharge_amount:
            return render(request, 'payments/recharge_result.html', {
                'error': 'Укажите карту и сумму пополнения.'
            })
        try:
            recharge_amount = Decimal(recharge_amount)  # Преобразование суммы в Decimal
        except Exception:
            return render(request, 'payments/recharge_result.html', {
                'error': 'Введите корректную сумму.'
            })
        card = get_object_or_404(Card, id=card_id, user=request.user)
        if recharge_amount > 0:
            card.balance += recharge_amount  # Добавляем сумму к балансу
            card.save()
            masked_card_number = '*' * (len(card.card_number) - 4) + card.card_number[-4:]# Маскировка всех цифр кроме последних 4 (типа как в настоящем банке)
            return render(request, 'payments/recharge_result.html', {
                'success': f"Баланс карты {masked_card_number}  успешно пополнен на {recharge_amount} Тг.",
                'redirect_url': 'user_cabinet'  
            })
        else:
            return render(request, 'payments/recharge_result.html', {
                'error': 'Сумма пополнения должна быть больше нуля.'
            })
    user_cards = Card.objects.filter(user=request.user)
    return render(request, 'payments/recharge_balance.html', {'cards': user_cards})

# Отображение всех карт пользователя 
@token_required
def card_list(request):
    cards = Card.objects.filter(user=request.user)
    return render(request, "payments/card_list.html", {"cards": cards})

# Выбор карты ,если она не одна и оплата рекламы  
@token_required
def select_card_payment(request, product_id, ad_type):
    error_message = " "
    product = get_object_or_404(Product, id=product_id)
    user_cards = request.user.cards.all() 
    price = AD_TYPE_PRICES.get(ad_type, 0)  # Цена рекламы
    if request.method == 'POST':
        selected_card_id = request.POST.get('card_id')  # Получаем ID выбранной карты
        if not selected_card_id:
            error_message = "Не выбрана карта для оплаты."
            return redirect('select_card_payment', product_id=product_id, ad_type=ad_type)
        card = get_object_or_404(Card, id=selected_card_id, user=request.user)
        if card.balance >= price:
            # Списываем средства
            card.balance -= price
            card.save()
            # Обновляем параметры рекламы
            if ad_type == 'top':
                product.added_to_top_at = timezone.now() # это для того чтобы потом правильно сортировать обьявления которые подняли вверх списка
            product.ad_expiration = timezone.now() + timedelta(days=1) # устанавливаем время действия рекламы
            product.save()
            # Создаем запись о платеже
            Payment.objects.create(
                user=request.user,
                card=card,
                amount=price,
                description=f"Оплата за {ad_type} рекламу для ножа {product}"
            )
            messages.success(request, f'Реклама успешно активирована! {price} Тг списано с карты.')
            return redirect('user_cabinet')
        else:
            error_message = 'Недостаточно средств на карте'
    return render(request, 'payments/select_card_payment.html',
    {   'product': product,
        'ad_type': ad_type,
        'cards': user_cards,
        'price': price,
        'error_message': error_message,
    })