from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import generic as view

# Create your views here.
from game_hub.games.forms import GameForm, CommentForm
from game_hub.games.models import Game, Comment


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


@login_required
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
    comments = game.comment_set.all()
    user = request.user

    is_owner = game.user == request.user

    context = {
        'game': game,
        'is_owner': is_owner,
        'comments': comments,
        'user': user,
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


class GameMyGames(LoginRequiredMixin, view.ListView):
    template_name = 'game_templates/game_my_games.html'
    model = Game
    context_object_name = 'games'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        my_games = Game.objects.filter(user_id=self.request.user.id)

        numbers_of_games = len(my_games)
        context['games'] = my_games
        context['numbers_of_games'] = numbers_of_games

        return context



# def game_my_games(request):
#     my_games = Game.objects.filter(pk=request.user.id)
#     numbers_of_my_games = len(my_games)
#
#     context = {
#         'my_games': my_games,
#         'numbers_of_my_games': numbers_of_my_games,
#     }
#     return render(request, 'game_templates/game_my_games.html', context)



# class CreateCommentView(view.CreateView):
#     template_name = 'game_templates/game_detail.html'
#     model = Comment
#     success_url = reverse_lazy('game details')


def create_comment(request, pk):
    game = Game.objects.get(pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = Comment(
            comment=form.cleaned_data['comment'],
            game=game,
            user=request.user,
        )
        comment.save()
        return redirect('game details', game.id)
