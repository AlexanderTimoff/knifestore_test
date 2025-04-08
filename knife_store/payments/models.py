from django.db import models
from django.conf import settings

class Card(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="cards"  
    )
    card_number = models.CharField(max_length=16, unique=True)
    bank = models.CharField(max_length=50, choices=[
        ('Kaspi Bank', 'Kaspi Bank'),
        ('RBK Bank', 'RBK Bank'),
        ('Halyk Bank', 'Halyk Bank'),
        ('Forte Bank', 'Forte Bank'),
        ('Jusan Bank', 'Jusan Bank'),
    ])
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - {self.bank} - {self.user.username}"
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} Тг - {self.user.username}"