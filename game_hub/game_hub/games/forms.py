import os

from django import forms

from game_hub.core.forms_bootstrap import BootstrapFormMixin
from game_hub.games.models import Game, Comment


class GameForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'category', 'max_level', 'image', 'description',)

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter game name'}),
            'max_level': forms.TextInput(attrs={'placeholder': 'Enter max level game/hero'}),
            'image': forms.FileInput(),
            'description': forms.Textarea(attrs={'placeholder': 'Enter descriptions', 'row': 3}),
        }


# class GameEditForm(BootstrapFormMixin, forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def save(self, *args):
#         file_path = self.instance.image.path
#         os.remove(file_path)
#
#     class Meta:
#         model = Game
#         fields = ('title', 'category', 'max_level', 'image', 'description',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
