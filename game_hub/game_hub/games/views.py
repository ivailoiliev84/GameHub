import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import generic as view

# Create your views here.
from game_hub.games.forms import GameForm, CommentForm
from game_hub.games.models import Game, Comment, LikeGame


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


# @login_required
# def game_create(request):
#     if request.method == 'POST':
#         form = GameForm(request.POST, request.FILES)
#         if form.is_valid():
#             game = form.save(commit=False)
#             game.user = request.user
#             game.save()
#             return redirect('catalogue list')
#     else:
#         form = GameForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'game_templates/game_create.html', context)


class GameCreateView(LoginRequiredMixin, view.FormView):
    form_class = GameForm
    template_name = 'game_templates/game_create.html'
    success_url = reverse_lazy('catalogue list')

    def form_valid(self, form):
        game = form.save(commit=False)
        game.user = self.request.user
        game.save()
        return super().form_valid(form)


# def game_details(request, pk):
#     game = Game.objects.get(pk=pk)
#     comments = game.comment_set.all()
#     user = game.user
#     like_game_count = game.likegame_set.count()
#
#     is_owner = game.user == request.user
#
#     context = {
#         'game': game,
#         'is_owner': is_owner,
#         'comments': comments,
#         'user': user,
#         'like_game_count': like_game_count,
#     }
#     return render(request, 'game_templates/game_detail.html', context)


class GameDetailsView(LoginRequiredMixin, view.DetailView):
    model = Game
    template_name = 'game_templates/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = context['game']

        is_owner = game.user == self.request.user
        comments = game.comment_set.all()
        user = self.request.user
        like_game_count = game.likegame_set.all().count()
        context['game'] = game
        context['is_owner'] = is_owner
        context['comments'] = comments
        context['user'] = user
        context['like_game_count'] = like_game_count

        return context


def game_edit(request, pk):
    game = Game.objects.get(pk=pk)
    old_picture = game.image.path

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            os.remove(old_picture)
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




def create_like(request, pk):
    game = Game.objects.get(pk=pk)
    user_whu_like = game.likegame_set.filter(user_id=request.user.id).first()

    if user_whu_like:
        user_whu_like.delete()
    else:
        like = LikeGame(
            game=game,
            user=request.user,
        )
        like.save()
    return redirect('game details', game.id)
