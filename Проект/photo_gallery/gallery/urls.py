from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),

    # Авторизация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Пользовательские функции
    path('upload/', views.upload_photo, name='upload_photo'),
    path('my-photos/', views.my_photos, name='my_photos'),
    path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),

    # AJAX функции
    path('photo/<int:photo_id>/like/', views.toggle_like, name='toggle_like'),
    path('photo/<int:photo_id>/comment/', views.add_comment, name='add_comment'),

    # Административные страницы
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-photos/', views.admin_photos, name='admin_photos'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-categories/', views.admin_categories, name='admin_categories'),

    # Административные действия
    path('admin-photos/<int:photo_id>/toggle-approval/', views.toggle_photo_approval, name='toggle_photo_approval'),
    path('admin-photos/<int:photo_id>/delete/', views.delete_photo_admin, name='delete_photo_admin'),
    path('admin-users/<int:user_id>/toggle-block/', views.toggle_user_block, name='toggle_user_block'),
    path('admin-categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
]