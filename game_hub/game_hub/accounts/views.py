from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import generic as view

# Create your views here.
from game_hub.accounts.forms import CreateGameHubUser, LoginForm, CreateProfileForm
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


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save_user()
            login(request, user)
            return redirect('catalogue list')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'accounts_templates/login_page.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


class ProfilePageView(view.TemplateView):
    template_name = 'profile_templates/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user_id=self.request.user.id)

        context['profile'] = profile
        return context


def profile_edit(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        form = CreateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
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
    if request.method == "POST":
        user.delete()
        profile.delete()
        return redirect('home')
    else:
        return render(request, 'profile_templates/profile_delete.html')

