from django import forms
from gallery.models import Category
from .models import ModeratedPhoto


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Нова категорія', 'class': 'form-control'})
        }


class ModeratedPhotoForm(forms.ModelForm):
    class Meta:
        model = ModeratedPhoto
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'rows': 4,
                'cols': 50,
                'placeholder': 'Причина блокування:',
                'class': 'form-control'
            }),
        }
