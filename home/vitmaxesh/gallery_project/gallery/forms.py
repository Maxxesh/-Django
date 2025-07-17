from django import forms
from .models import Photo, Comment


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
