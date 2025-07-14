from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Ви вийшли з акаунту.')
    return redirect('users:login')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm
    success_url = reverse_lazy('gallery:home')

    def form_valid(self, form):
        user = form.get_user()
        if user.is_blocked:
            return render(self.request, 'users/blocked.html', {})
        login(self.request, user)
        messages.success(self.request, f"Ласкаво просимо, {user.username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Неправильне ім'я користувача або пароль. Будь ласка, спробуйте ще раз.")
        return super().form_invalid(form)
