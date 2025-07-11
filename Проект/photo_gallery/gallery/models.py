from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    """Расширенная модель пользователя"""
    full_name = models.CharField(max_length=100, verbose_name="ПІБ")
    city = models.CharField(max_length=50, verbose_name="Місто")
    country = models.CharField(max_length=50, verbose_name="Країна")
    nickname = models.CharField(max_length=30, unique=True, verbose_name="Нікнейм")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокований")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nickname

class Category(models.Model):
    """Категории фотографий"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

class Photo(models.Model):
    """Модель фотографии"""
    title = models.CharField(max_length=200, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    image = models.ImageField(upload_to='photos/', verbose_name="Фотографія")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0, verbose_name="Перегляди")

    class Meta:
        verbose_name = "Фотографія"
        verbose_name_plural = "Фотографії"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.like_set.count()

    def get_comments_count(self):
        return self.comment_set.count()

class Like(models.Model):
    """Лайки для фотографий"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')

    def __str__(self):
        return f"{self.user.nickname} likes {self.photo.title}"

class Comment(models.Model):
    """Комментарии к фотографиям"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.nickname}: {self.text[:50]}..."