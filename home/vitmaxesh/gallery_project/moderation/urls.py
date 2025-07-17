from django.urls import path
from . import views
app_name = 'moderation'
urlpatterns = [
    path('', views.moderation_page, name='moderate'),
    path('api/categories/<int:category_id>/',
         views.update_category_api, name='update_category_api'),
    path('api/categories/delete/<int:category_id>/',
         views.delete_category_api, name='delete_category_api'),
    path('photo/<int:pk>/moderate/', views.moderate_photo, name='moderate_photo'),
    path('photo/<int:pk>/approve/', views.approve_photo, name='approve_photo'),
    path('user/<int:pk>/block/', views.block_user, name='block_user'),
    path('photo_list', views.photo_list, name='photo_list'),
    path('user_list', views.user_list, name='user_list'),
    path('user_detail/<int:pk>', views.user_detail, name='user_detail'),
]
