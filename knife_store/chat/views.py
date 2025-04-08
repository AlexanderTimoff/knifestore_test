from django.shortcuts import redirect, get_object_or_404,render
from django.http import HttpResponseRedirect
from django.db import models

from .models import Chat, Message
from users.models import CustomUser
from users.decorators import token_required
from products.models import Product


@token_required
def start_chat(request, seller_id, product_id):
    seller = get_object_or_404(CustomUser, id=seller_id)
    buyer = request.user
    product = get_object_or_404(Product, id=product_id)
    
    # Если это мое обьявление , выдаем ошибку так как самому себе нельзя писать
    if buyer.id == seller_id:
        return render(request, 'chat/error.html', {'error_message': 'Это ваше объявление'})
    chat = Chat.objects.filter(buyer=buyer, seller=seller, product=product).first()
    # Если чат уже существует, перенаправляем на страницу чата
    if chat:
        # Если чат неактивен, активируем его
        if not chat.is_active:
            chat.is_active = True
            chat.save()
        return redirect('chat:chat_room', chat_id=chat.id)
    # Если чат не существует, создаем новый 
    if request.method == 'GET':
        chat = Chat.objects.create(buyer=buyer, seller=seller, product=product, is_active=False)
        return render(request, 'chat/chat_room.html', {'chat': chat, 'seller': seller, 'product': product})
    #Если нажали на отправку сообщения
    elif request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            # Если чат не существует, создаем новый и делаем его активным
            if not chat:
                chat = Chat.objects.create(buyer=buyer, seller=seller, product=product, is_active=True)
            # Создаем первое сообщение
            message = Message.objects.create(chat=chat, sender=buyer, text=message_text)
            print(f"Создано первое сообщение: {message.text}")  # Отладка
            return redirect('chat:chat_room', chat_id=chat.id)
        else:
            return render(request, 'chat/error.html', {'error': 'Сообщение не может быть пустым'})
    # Если не было отправлено сообщения, просто показываем страницу чата
    return render(request, 'chat/chat_room.html', {'seller': seller, 'product': product})

@token_required
def chat_room(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.order_by('created_at')  # Сортировка сообщений
    return render(request, 'chat/chat_room.html', {'chat': chat, 'messages': messages})

@token_required
def send_message(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id=chat_id)
        text = request.POST.get('message')
        if text:
            # Создание нового сообщения
            Message.objects.create(chat=chat, sender=request.user, text=text)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Перенаправление обратно на тот же чат

@token_required
def chat_list(request):
    user = request.user
    # Получаем чаты, где пользователь является покупателем или продавцом, но не с самим собой
    chats = Chat.objects.filter(models.Q(buyer=user) | models.Q(seller=user)).exclude(
        models.Q(buyer=user, seller=user)
    ).filter(is_active=True).select_related('product', 'buyer', 'seller')
    return render(request, 'chat/chat_list.html', {'chats': chats})