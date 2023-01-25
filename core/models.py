from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'
