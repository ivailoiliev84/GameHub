from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import generic as view

# Create your views here.
from game_hub.accounts.forms import CreateGameHubUser, LoginForm


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
