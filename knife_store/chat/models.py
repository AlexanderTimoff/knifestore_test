from django.db import models

from products.models import Product
from users.models import CustomUser


class Chat(models.Model):
    buyer = models.ForeignKey(CustomUser, related_name='chats_as_buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, related_name='chats_as_seller', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
