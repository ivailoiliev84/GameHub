import os

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import generic as view, View

# Create your views here.
from game_hub.accounts.forms import CreateGameHubUser, CreateProfileForm
from game_hub.accounts.models import Profile

GameHubUser = get_user_model()


class RegisterUser(view.CreateView):
    form_class = CreateGameHubUser
    template_name = 'accounts_templates/register_page.html'
    success_url = reverse_lazy('catalogue list')

    def form_valid(self, form):
        user = super().form_valid(form)
        login(self.request, self.object)
        return user


class LoginUserView(LoginView):
    template_name = 'accounts_templates/login_page.html'

    def get_success_url(self):
        return reverse_lazy('catalogue list')


def logout_user(request):
    logout(request)
    return redirect('home')


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'profile_templates/change_password.html'
    success_url = reverse_lazy('profile')


class ProfilePageView(view.TemplateView):
    template_name = 'profile_templates/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user_id=self.request.user.id)

        context['profile'] = profile
        return context


class ProfileEditView(view.FormView):
    pass


def profile_edit(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.profile_picture:
        old_picture = profile.profile_picture.path
    else:
        old_picture = None
    if request.method == 'POST':
        form = CreateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if old_picture:
                os.remove(old_picture)
                form.save()
            else:
                form.save()
            return redirect('profile')
    else:
        form = CreateProfileForm(instance=profile)
    context = {
        'form': form
    }
    return render(request, 'profile_templates/profile_edit.html', context)


def profile_delete(request):
    profile = Profile.objects.get(user_id=request.user.id)
    user = request.user
    if profile.profile_picture:
        old_picture = profile.profile_picture.path
    else:
        old_picture = None
    if request.method == "POST":
        if old_picture:
            os.remove(old_picture)
            user.delete()
            profile.delete()
            return redirect('home')
        else:
            user.delete()
            profile.delete()
            return redirect('home')
    else:

        context = {
            'user': user,
        }
        return render(request, 'profile_templates/profile_delete.html', context)
