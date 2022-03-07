from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import generic as view

# Create your views here.
from game_hub.games.forms import GameForm
from game_hub.games.models import Game


class HomeView(view.TemplateView):
    template_name = 'base/home_page.html'


class CatalogueListView(LoginRequiredMixin, view.ListView):
    template_name = 'game_templates/game_catalogue.html'
    model = Game
    context_object_name = 'games'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.all()
        return context


def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()
            return redirect('catalogue list')
    else:
        form = GameForm()
    context = {
        'form': form
    }
    return render(request, 'game_templates/game_create.html', context)


def game_details(request, pk):
    game = Game.objects.get(pk=pk)

    is_owner = game.id == request.user.id

    context = {
        'game': game,
        'is_owner': is_owner,
    }
    return render(request, 'game_templates/game_detail.html', context)


def game_edit(request, pk):
    game = Game.objects.get(pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game details', game.id)
    else:
        form = GameForm(instance=game)

    context = {
        'form': form,
        'game': game,
    }
    return render(request, 'game_templates/game_edit.html', context)


def delete_game(request, pk):
    game = Game.objects.get(pk=pk)
    game.delete()
    return redirect('catalogue list')
