from django.urls import path
from .views import start_chat, chat_room,send_message,chat_list

app_name = 'chat'

urlpatterns = [
    path('start/<int:seller_id>/<int:product_id>/', start_chat, name='start_chat'),
    path('room/<int:chat_id>/', chat_room, name='chat_room'),
    path('send/<int:chat_id>/', send_message, name='send_message'),
    path('list/', chat_list, name='chat_list'),
]