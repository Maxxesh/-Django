from django.urls import path
from . import views
app_name = 'gallery'
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_photo, name='upload'),
    path('photo/<int:pk>/', views.view_photo, name='photo_detail'),
    path('photo/<int:pk>/like/', views.like_photo, name='like_photo'),
]
