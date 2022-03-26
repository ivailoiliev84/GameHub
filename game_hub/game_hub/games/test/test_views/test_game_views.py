from django.test import TestCase
from django.urls import reverse, reverse_lazy


class TestHomePageViews(TestCase):

    def test_home_view_should_be_rendering_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'base/home_page.html')


class TestGameTemplatesViews(TestCase):

    def test_catalogue_list_view(self):
        response = self.client.get(reverse('catalogue list'))
        self.assertTemplateUsed(response, 'game_templates/game_catalogue.html')


class TestGameCreateView(TestCase):

    def test_game_create_view_should_create_game(self):
        response = self.client.get(reverse('create game'))
        self.assertTemplateUsed(response, 'game_templates/game_create.html')
