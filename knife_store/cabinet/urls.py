from django.urls import path
from .views import user_cabinet

urlpatterns = [
    path('cabinet/', user_cabinet, name='user_cabinet'),
]
