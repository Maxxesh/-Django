from django.contrib import admin
from .models import CustomUser, Category, Photo, Like, Comment

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'email', 'is_blocked')
    list_filter = ('is_blocked', 'created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'uploaded_at')
    list_filter = ('category', 'uploaded_at')

admin.site.register(Like)
admin.site.register(Comment)