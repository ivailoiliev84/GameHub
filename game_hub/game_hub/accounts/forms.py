from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from game_hub.accounts.models import Profile

UserModel = get_user_model()


class CreateGameHubUser(UserCreationForm):
    bot_catcher = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def clean_bot_catcher(self):
        bot_catcher = self.cleaned_data['bot_catcher']
        if bot_catcher:
            raise forms.ValidationError('Bot detected')

    class Meta:
        model = UserModel
        fields = ('email',)

        # widgets = {
        #     'email': forms.TextInput(attrs={'placeholder': 'email', 'id': 'email'})
        # }


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput()
    )

    user = None

    def clean_password(self):
        self.user = authenticate(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']

        )
        if not self.user:
            raise ValidationError('Email and/or password are incorrect')

    def save_user(self):
        return self.user


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
