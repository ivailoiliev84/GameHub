from django.urls import path

from game_hub.games.views import HomeView, CatalogueListView, game_edit, delete_game, \
    create_comment, GameMyGames, create_like, GameCreateView, GameDetailsView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('catalogue/', CatalogueListView.as_view(), name='catalogue list'),
    path('create-game/', GameCreateView.as_view(), name='create game'),
    path('details/<int:pk>', GameDetailsView.as_view(), name='game details'),
    path('edit/<int:pk>', game_edit, name='game edit'),
    path('delete/<int:pk>', delete_game, name='delete game'),
    path('game/my-games', GameMyGames.as_view(), name='my games'),
    # path('game/mygame', game_my_games, name='my games'),

    path('comment/<int:pk>', create_comment, name='create comment'),
    path('like-game/<int:pk>', create_like, name='like game'),

)
