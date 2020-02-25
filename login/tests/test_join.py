from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse
from login.models import User


class JoinTest(TestCase):
    """ Test Join """

    def setUp(self):
        """ Before every test """
        self.client = Client()
        self.join_url = reverse('login:join')
        # Create a new user.
        self.user = User.objects.create(email='user_test@django.test')
        self.user.set_password('@december2019')
        self.user.save()

    def test_join_url_and_template(self):
        response = self.client.get(self.join_url)
        self.assertTemplateUsed(response, 'registration/join.html')
        self.assertEqual(response.status_code, 200)

    def test_join_form_valid(self):
        """ Create a new user. """
        response = self.client.post(self.join_url, {
            'email': 'new_user@django.fr',
            'password1': '@jesuisNouveau',
            'password2': '@jesuisNouveau'
        })
        self.assertRedirects(
            response, '/login/mypage/',
            status_code=302, target_status_code=200)

    def test_join_form_invalid(self):
        """ The passwords don't match. """
        response = self.client.post(self.join_url, {
            'email': 'new_user',
            'password1': '@jesuisNouveau',
            'password2': '@jesuisNouveau200'
        })
        self.assertEqual(response.status_code, 200)

    def test_join_user_already_exist(self):
        try:
            user = User.objects.create(email='user_test@django.test')
            user.set_password('@jesuisNouveau')
            user.save()

        except IntegrityError:
            user = False

        self.assertFalse(user)
