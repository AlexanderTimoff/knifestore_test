from django.contrib import admin
from .models import Payment, Card

admin.site.register(Card)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'description', 'created_at')  # Показываем время платежа
    list_filter = ('created_at', 'user') 