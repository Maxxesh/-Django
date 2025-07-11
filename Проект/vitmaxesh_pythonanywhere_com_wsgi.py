import os
import sys

# Путь к вашему проекту
project_home = '/home/vitmaxesh/photo_gallery'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photo_gallery.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()