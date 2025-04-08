from django.urls import path
from .views import add_card,card_list,delete_card,select_card_payment,recharge_balance

urlpatterns = [
    path('add-card/', add_card, name='add_card'), 
    path('cards/', card_list, name='card_list'), 
    path('delete_card/<int:card_id>/', delete_card, name='delete_card'), 
    path('recharge/', recharge_balance, name='recharge_balance'),
    path('promote/select_card/<int:product_id>/<str:ad_type>/', select_card_payment, name='select_card_payment'),
]
