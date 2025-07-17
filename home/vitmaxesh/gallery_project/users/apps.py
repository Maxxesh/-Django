from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'  # Должно совпадать с именем папки
    label = 'users'  # Убедитесь, что это 'users', а не 'my_users'