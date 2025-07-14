from django.contrib import custom_admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('gallery.urls')),
    path('admin/', custom_admin.site.urls),
    path('users/', include('users.urls')),
    path('admin-panel/', include('admin.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
