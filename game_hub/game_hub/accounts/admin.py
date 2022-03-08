from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from game_hub.accounts.models import GameHubUserManager, Profile
from game_hub.games.models import Game

GameUser = get_user_model()


class ProfileInlineAdmin(admin.StackedInline):
    model = Profile


class GmeInlineAdmin(admin.StackedInline):
    model = Game


@admin.register(GameUser)
class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInlineAdmin,)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
