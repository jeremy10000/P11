from django.test import TestCase, Client
from django.urls import reverse

from product.models import Product
from login.models import User


class FavoritesViewTest(TestCase):
    """ Test FavoritesView """
    fixtures = ["products.json"]

    def setUp(self):
        self.client = Client()
        self.favorites_url = reverse('product:favorites')
        self.save_url = reverse('product:save')
        # Create a new user.
        user = User.objects.create(email='t@mail.fr')
        user.set_password('mdp')
        user.save()

    def test_favorites_redirect_if_not_logged(self):
        response = self.client.get(self.favorites_url)
        self.assertRedirects(
            response, '/login?next=/product/favorites/',
            status_code=302, target_status_code=301)

    def test_favorites_if_logged_and_zero_product(self):
        self.client.login(
            username='t@mail.fr',
            password='mdp')

        response = self.client.get(self.favorites_url)

        self.assertTemplateUsed(response, 'product/favorites.html')
        self.assertEqual(response.context_data["object_list"].count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_favorites_if_logged_and_one_product(self):
        self.client.login(
            username='t@mail.fr',
            password='mdp')

        user_id = User.objects.get(email='t@mail.fr').id

        response = self.client.get(self.favorites_url)
        self.assertEqual(response.context_data["object_list"].count(), 0)

        response = self.client.post(
            self.save_url, {
                'product_id': Product.objects.get(id=1).id,
                'substitute_id': Product.objects.get(id=2).id,
                'user_id': user_id,
                'next': '/',
            }
        )

        response = self.client.get(self.favorites_url)
        self.assertEqual(response.context_data["object_list"].count(), 1)
        self.assertEqual(response.status_code, 200)
