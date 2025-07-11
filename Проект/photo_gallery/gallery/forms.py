from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Photo, Comment, Category

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True, label='ПІБ')
    city = forms.CharField(max_length=50, required=True, label='Місто')
    country = forms.CharField(max_length=50, required=True, label='Країна')
    nickname = forms.CharField(max_length=50, required=True, label='Нікнейм')

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'city', 'country', 'nickname', 'password1', 'password2')
        labels = {
            'username': 'Ім\'я користувача',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Підтвердження пароля'
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'description', 'category', 'image')
        labels = {
            'title': 'Назва фотографії',
            'description': 'Опис',
            'category': 'Категорія',
            'image': 'Фотографія'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем пустую опцию для категории
        self.fields['category'].empty_label = 'Оберіть категорію'
        self.fields['category'].queryset = Category.objects.all()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Ваш коментар'
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишіть ваш коментар...'
            })
        }