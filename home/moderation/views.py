from django.shortcuts import render, redirect, get_object_or_404
from gallery.models import Category, Photo, CustomUser
from users.models import CustomUser
from .models import ModeratedPhoto
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from .forms import CategoryForm, ModeratedPhotoForm
from django.db.models import Count


@staff_member_required
def moderation_page(request):
    print(request.user)
    total_photos = Photo.objects.count()
    total_users = CustomUser.objects.count()
    categories = Category.objects.all()
    form = CategoryForm()
    users_with_photo_counts = CustomUser.objects.annotate(
        uploaded_photo_count=Count('photo'))
    users_with_photo_counts = users_with_photo_counts.order_by(
        '-uploaded_photo_count')
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('moderation:moderate')
    return render(request, 'moderation/moderation_page.html', {'total_photos': total_photos,
                                                               'total_users': total_users,
                                                               'categories': categories,
                                                               'form': form,
                                                               'users_with_photo_counts': users_with_photo_counts
                                                               })


@staff_member_required
def update_category_api(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id)
        data = json.loads(request.body)
        new_name = data.get('name')

        if not new_name or not isinstance(new_name, str) or not new_name.strip():
            return JsonResponse({'message': "Ім'я категорії не може бути порожнім."}, status=400)

        category.name = new_name.strip()
        category.save()

        return JsonResponse({'id': category.id, 'name': category.name}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Невірний формат JSON у тілі запиту.'}, status=400)
    except Exception as e:
        print(f"Ошибка при обновлении категории: {e}")
        return JsonResponse({'message': 'Внутрішня помилка сервера.'}, status=500)


@staff_member_required
@require_http_methods(["DELETE"])
def delete_category_api(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id)
        category_name = category.name
        category.delete()
        return JsonResponse(
            {'message': f'Категорія "{category_name}" успішно видалена.',
                'id': category_id},
            status=200
        )
    except Category.DoesNotExist: 
        return JsonResponse({'message': 'Категорія не знайдена.'}, status=404)
    except Exception as e:
        print(f"Ошибка при видаленні категории ID {category_id}: {e}")
        return JsonResponse({'message': 'Внутрішня помилка сервера при видаленні.'}, status=500)


@staff_member_required
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'moderation/photo_list.html', {'photos': photos})


@staff_member_required
def moderate_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        moderated_entry = ModeratedPhoto.objects.filter(photo=photo).first()
        if not (moderated_entry):
            ModeratedPhoto.objects.create(photo=photo, reason=reason)
        photo.is_approved = False
        photo.save()
        return redirect('gallery:home')
    form = ModeratedPhotoForm()
    return render(request, 'moderation/moderate_photo.html', {'photo': photo, 'form': form})


@staff_member_required
def approve_photo(request, pk):
    try:
        photo = get_object_or_404(Photo, pk=pk)
        moderated_entry = ModeratedPhoto.objects.filter(photo=photo).first()
        if moderated_entry:
            try:
                moderated_entry.delete()
            except Exception as e:
                print(f'Помилка при видаленні ModeratedPhoto: {e}')
        photo.is_approved = True
        photo.save()
    except Exception as e:
        print('Помилка', e)
    return redirect('gallery:home')


@staff_member_required
def block_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if user.is_blocked == False:
        user.is_blocked = True
    else:
        user.is_blocked = False
    user.save()
    return redirect('moderation:user_list')


@staff_member_required
def user_list(request):
    users = CustomUser.objects.filter(is_staff=False)
    return render(request, 'moderation/user_list.html', {'users': users})


@staff_member_required
def user_detail(request, pk):
    try:
        user = get_object_or_404(CustomUser, pk=pk)
    except Exception as e:
        print(e)
    return render(request, 'moderation/detail_user.html', {'user': user})
