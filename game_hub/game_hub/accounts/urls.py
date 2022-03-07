from django.urls import path

from game_hub.accounts.views import RegisterUser, logout_user, login_user

urlpatterns = (
    path('register/', RegisterUser.as_view(), name='register'),
    path('log-in/', login_user, name='login'),
    path('log-out', logout_user, name='logout'),
)

