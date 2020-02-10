from django.test import TestCase, Client
from django.urls import reverse

from product.models import Product
from login.models import User


class DeleteViewTest(TestCase):
    """ DeleteView """
    fixtures = ["products.json"]

    def setUp(self):
        self.client = Client()
        self.save_url = reverse('product:save')
        self.favorites_url = reverse('product:favorites')
        # Create a new user.
        user = User.objects.create(email='t@mail.fr')
        user.set_password('mdp')
        user.save()

    def test_delete_if_not_logged(self):
        response = self.client.post("/product/delete/1000")
        self.assertRedirects(
            response, '/login?next=/product/delete/1000',
            status_code=302, target_status_code=301)

    def test_delete_if_logged_and_unknown_id(self):
        self.client.login(
            username='t@mail.fr',
            password='mdp')

        response = self.client.post("/product/delete/1000")
        self.assertEqual(response.status_code, 404)

    def test_delete_success(self):
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

        response = self.client.post("/product/delete/1")
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.favorites_url)
        self.assertEqual(response.context_data["object_list"].count(), 0)
