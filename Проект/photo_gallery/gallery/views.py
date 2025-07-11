from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Photo, Category, Comment, Like, UserProfile
from .forms import PhotoUploadForm, CommentForm, UserRegistrationForm
import json

def home(request):
    """Главная страница с последними фотографиями"""
    photos = Photo.objects.filter(is_approved=True).order_by('-created_at')[:12]
    categories = Category.objects.all()
    return render(request, 'gallery/home.html', {
        'photos': photos,
        'categories': categories
    })

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаем профиль пользователя
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country'],
                nickname=form.cleaned_data['nickname']
            )
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def gallery(request):
    """Страница галереи с фильтрацией и сортировкой"""
    photos = Photo.objects.filter(is_approved=True)

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        photos = photos.filter(category_id=category_id)

    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        photos = photos.order_by('created_at')
    elif sort_by == 'popular':
        photos = photos.annotate(likes_count=Count('likes')).order_by('-likes_count')
    elif sort_by == 'most_commented':
        photos = photos.annotate(comments_count=Count('comments')).order_by('-comments_count')
    else:  # newest
        photos = photos.order_by('-created_at')

    # Пагинация
    paginator = Paginator(photos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'gallery/gallery.html', {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_id,
        'current_sort': sort_by
    })

def photo_detail(request, photo_id):
    """Детальная страница фотографии"""
    photo = get_object_or_404(Photo, id=photo_id, is_approved=True)
    comments = Comment.objects.filter(photo=photo).order_by('-created_at')

    # Проверяем, лайкнул ли пользователь эту фотографию
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(photo=photo, user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.photo = photo
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('photo_detail', photo_id=photo.id)
    else:
        comment_form = CommentForm()

    return render(request, 'gallery/photo_detail.html', {
        'photo': photo,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked
    })

@login_required
def upload_photo(request):
    """Загрузка фотографии"""
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, 'Фотография загружена и отправлена на модерацию!')
            return redirect('gallery')
    else:
        form = PhotoUploadForm()

    return render(request, 'gallery/upload.html', {'form': form})

@login_required
def toggle_like(request, photo_id):
    """AJAX обработка лайков"""
    if request.method == 'POST':
        photo = get_object_or_404(Photo, id=photo_id)
        like, created = Like.objects.get_or_create(photo=photo, user=request.user)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        likes_count = Like.objects.filter(photo=photo).count()

        return JsonResponse({
            'liked': liked,
            'likes_count': likes_count
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def user_profile(request):
    """Профиль пользователя"""
    user_photos = Photo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'gallery/profile.html', {
        'user_photos': user_photos
    })

# Административные представления
@staff_member_required
def admin_dashboard(request):
    """Панель администратора"""
    total_photos = Photo.objects.count()
    pending_photos = Photo.objects.filter(is_approved=False).count()
    total_users = UserProfile.objects.count()
    active_users = UserProfile.objects.filter(is_blocked=False).count()

    # Статистика по категориям
    category_stats = Category.objects.annotate(
        photos_count=Count('photo')
    ).order_by('-photos_count')

    return render(request, 'admin/dashboard.html', {
        'total_photos': total_photos,
        'pending_photos': pending_photos,
        'total_users': total_users,
        'active_users': active_users,
        'category_stats': category_stats
    })

@staff_member_required
def manage_photos(request):
    """Управление фотографиями"""
    photos = Photo.objects.all().order_by('-created_at')

    # Фильтрация
    status = request.GET.get('status')
    if status == 'pending':
        photos = photos.filter(is_approved=False)
    elif status == 'approved':
        photos = photos.filter(is_approved=True)

    paginator = Paginator(photos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/manage_photos.html', {
        'page_obj': page_obj,
        'current_status': status
    })

@staff_member_required
def approve_photo(request, photo_id):
    """Одобрение фотографии"""
    photo = get_object_or_404(Photo, id=photo_id)
    photo.is_approved = True
    photo.save()
    messages.success(request, f'Фотография "{photo.title}" одобрена!')
    return redirect('manage_photos')

@staff_member_required
def delete_photo(request, photo_id):
    """Удаление фотографии"""
    photo = get_object_or_404(Photo, id=photo_id)
    photo.delete()
    messages.success(request, f'Фотография "{photo.title}" удалена!')
    return redirect('manage_photos')

@staff_member_required
def manage_users(request):
    """Управление пользователями"""
    users = UserProfile.objects.all().order_by('-created_at')

    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/manage_users.html', {
        'page_obj': page_obj
    })

@staff_member_required
def toggle_user_block(request, user_id):
    """Блокировка/разблокировка пользователя"""
    user_profile = get_object_or_404(UserProfile, id=user_id)
    user_profile.is_blocked = not user_profile.is_blocked
    user_profile.save()

    action = "заблокирован" if user_profile.is_blocked else "разблокирован"
    messages.success(request, f'Пользователь {user_profile.user.username} {action}!')

    return redirect('manage_users')

@staff_member_required
def manage_categories(request):
    """Управление категориями"""
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if name:
            Category.objects.create(name=name, description=description)
            messages.success(request, f'Категория "{name}" создана!')

        return redirect('manage_categories')

    return render(request, 'admin/manage_categories.html', {
        'categories': categories
    })

@staff_member_required
def delete_category(request, category_id):
    """Удаление категории"""
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, f'Категория "{category.name}" удалена!')
    return redirect('manage_categories')