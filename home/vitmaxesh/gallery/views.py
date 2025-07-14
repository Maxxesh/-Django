from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Photo, Category
from .forms import PhotoUploadForm, CommentForm
from users.models import CustomUser
from django.db.models import Count


def home(request):
    category_request = request.GET.get('category')
    sort_request = request.GET.get('sort')
    categories = Category.objects.all()
    photos = Photo.objects.filter(is_approved=True)
    if category_request:
        photos = photos.filter(category__name=category_request)
    if sort_request == 'likes':
        photos = photos.annotate(
            num_likes=Count('likes')).order_by('-num_likes')
    elif sort_request == 'date':
        photos = photos.order_by('-created_at')
    return render(request, 'gallery/home.html', {'photos': photos,
                                                 'categories': categories,
                                                 'selected_category': category_request, 
                                                 'selected_sort': sort_request, })


@login_required
def upload_photo(request):
    if request.user.is_blocked:
        return render(request, 'gallery/blocked.html')
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.author = request.user
            photo.save()
            form.save_m2m()
            return redirect('gallery:home')
    else:
        form = PhotoUploadForm()
    return render(request, 'gallery/upload.html', {'form': form})


def view_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    comments = photo.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.photo = photo
            comment.save()
            return redirect('gallery:photo_detail', pk=pk)
    else:
        comment_form = CommentForm()
    return render(request, 'gallery/view_photo.html', {'photo': photo, 'comments': comments, 'form': comment_form})


@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return redirect('gallery:photo_detail', pk=pk)
