from django.db import models
from django.conf import settings
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField('Назва', max_length=100, unique=True)

    def __str__(self):
        return self.name

    def photo_count(self):
        return self.photo_set.count()


class Photo(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked_photos', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    photo = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"
