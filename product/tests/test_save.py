from django.test import TestCase, Client
from django.urls import reverse

from product.models import Category, Level, Product, Substitute
from login.models import User


class SaveViewTest(TestCase):
    """ Test SaveView """
    fixtures = ["products.json"]

    def setUp(self):
        self.client = Client()
        self.save_url = reverse('product:save')
        # Create a new user.
        user = User.objects.create(email='t@mail.fr')
        user.set_password('mdp')
        user.save()

    def test_save_valid_post_if_not_logged(self):
        user_id = User.objects.get(email='t@mail.fr').id
        response = self.client.post(
            self.save_url, {
                'product_id': Product.objects.get(id=1).id,
                'substitute_id': Product.objects.get(id=2).id,
                'user_id': user_id,
                'next': '/',
            }
        )
        self.assertRedirects(
            response, '/login/',
            status_code=302, target_status_code=200)

    def test_save_success_and_error_if_logged(self):
        self.client.login(
            username='t@mail.fr',
            password='mdp')

        user_id = User.objects.get(email='t@mail.fr').id

        self.assertEqual(Substitute.objects.all().count(), 0)

        response = self.client.post(
            self.save_url, {
                'product_id': Product.objects.get(id=1).id,
                'substitute_id': Product.objects.get(id=2).id,
                'user_id': user_id,
                'next': '/',
            }
        )

        self.assertEqual(Substitute.objects.all().count(), 1)
        self.assertRedirects(
            response, '/product/favorites/',
            status_code=302, target_status_code=200)

        response = self.client.post(
            self.save_url, {
                'product_id': Product.objects.get(id=1).id,
                'substitute_id': Product.objects.get(id=2).id,
                'user_id': user_id,
                'next': '/',
            }, follow=True
        )

        self.assertEqual(Substitute.objects.all().count(), 1)

        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "info")
        self.assertTrue(message.message, "Le produit est déja enregistré !")

    def test_save_invalid_post(self):
        user_id = User.objects.get(email='t@mail.fr').id
        with self.assertRaises(Product.DoesNotExist):
            response = self.client.post(
                self.save_url, {
                    'product_id': Product.objects.get(id=10).id,
                    'substitute_id': Product.objects.get(id=2).id,
                    'user_id': user_id,
                }
            )
