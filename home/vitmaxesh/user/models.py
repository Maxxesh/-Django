from django.contrib.auth.models import AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_blocked = models.BooleanField(default=False)



