
from django.db import models
from django.contrib.auth.models import AbstractUser


# используем стандартную джанго модель юсера и добавляем пару полей 
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    reset_code = models.CharField(max_length=4, blank=True, null=True)
    def __str__(self):
        return self.username
