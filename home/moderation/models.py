from django.db import models
from gallery.models import Photo


class ModeratedPhoto(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)
    reason = models.TextField()
    moderated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заблоковано: {self.photo.title}"
