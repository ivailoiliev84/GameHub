from django import forms

from game_hub.games.models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'category', 'max_level', 'image', 'description',)

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter game name'}),
            'max_level': forms.TextInput(attrs={'placeholder': 'Enter max level game/hero'}),
            'image': forms.FileInput(),
            'description': forms.Textarea(attrs={'placeholder': 'Enter descriptions', 'row': 3}),
        }
