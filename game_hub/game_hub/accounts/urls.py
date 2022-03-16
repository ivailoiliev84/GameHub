from django.urls import path

from game_hub.accounts.views import RegisterUser, logout_user, ProfilePageView, profile_edit, \
    profile_delete, LoginUserView, ChangePasswordView

urlpatterns = (
    path('register/', RegisterUser.as_view(), name='register'),
    path('log-in/', LoginUserView.as_view(), name='login'),
    path('log-out/', logout_user, name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change password'),

    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('profile-edit/', profile_edit, name='profile edit'),
    path('profile-delte/', profile_delete, name='profile delete')
)
