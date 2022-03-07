from django.urls import path

from game_hub.games.views import HomeView, CatalogueListView, game_create, game_details, game_edit, delete_game, \
    GameMyGames

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('catalogue/', CatalogueListView.as_view(), name='catalogue list'),
    path('create-game/', game_create, name='create game'),
    path('details/<int:pk>', game_details, name='game details'),
    path('edit/<int:pk>', game_edit, name='game edit'),
    path('delete/<int:pk>', delete_game, name='delete game'),
    path('game/my-games', GameMyGames.as_view(), name='my games'),

)
