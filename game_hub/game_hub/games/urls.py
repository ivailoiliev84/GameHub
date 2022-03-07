from django.urls import path

from game_hub.games.views import HomeView, CatalogueListView, game_create

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('catalogue/', CatalogueListView.as_view(), name='catalogue list'),
    path('create-game/', game_create, name='create game')

)
