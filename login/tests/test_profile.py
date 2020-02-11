from django.test import TestCase, Client
from django.urls import reverse
from login.models import User


class ProfileTest(TestCase):
    """ Test: Change the profile. """

    def setUp(self):
        """ Before every test """
        self.client = Client()
        self.profile_url = reverse('login:update')
        self.password_url = reverse('login:change_pwd')
        # Create a new user.
        self.user = User.objects.create(
            email='usertest@t.fr',
            first_name='Prénom',
            last_name='Nom')
        self.user.set_password('Deux2020')
        self.user.save()

    def test_if_the_user_is_not_logged_in(self):
        """ Test redirection """
        response = self.client.get(self.profile_url)
        self.assertRedirects(
            response, '/login?next=/login/change-profile/',
            status_code=302, target_status_code=301)

        response = self.client.get(self.password_url)
        self.assertRedirects(
            response, '/login?next=/login/change-password/',
            status_code=302, target_status_code=301)

    def test_change_name(self):
        """ Change the first and last name. """
        self.client.login(username='usertest@t.fr', password='Deux2020')

        first_name = User.objects.get(email="usertest@t.fr").first_name
        last_name = User.objects.get(email="usertest@t.fr").last_name
        # Original names.
        self.assertEqual(first_name, "Prénom")
        self.assertEqual(last_name, "Nom")

        # Apply a change.
        response = self.client.post(self.profile_url, {
            "first_name": "Nouveau Prénom",
            "last_name": "Nouveau Nom"
        })
        # Redirection
        self.assertRedirects(
            response, '/login/mypage/',
            status_code=302, target_status_code=200)

        first_name = User.objects.get(email="usertest@t.fr").first_name
        last_name = User.objects.get(email="usertest@t.fr").last_name
        # New names.
        self.assertEqual(first_name, "Nouveau Prénom")
        self.assertEqual(last_name, "Nouveau Nom")

    def test_change_password(self):
        """ Change the password. """
        self.client.login(username='usertest@t.fr', password='Deux2020')

        # Check the original password.
        user = User.objects.get(email='usertest@t.fr')
        self.assertEqual(user.check_password('Deux2020'), True)

        # Apply a change.
        response = self.client.post(self.password_url, {
            "old_password": "Deux2020",
            "new_password1": "Trois2121",
            "new_password2": "Trois2121"
        })
        # Redirection
        self.assertRedirects(
            response, '/login/change-password/done/',
            status_code=302, target_status_code=200)

        # Check the new password.
        user = User.objects.get(email='usertest@t.fr')
        self.assertEqual(user.check_password('Trois2121'), True)

    def test_change_password_error(self):
        """ Password change failed. """
        self.client.login(username='usertest@t.fr', password='Deux2020')

        # Check the original password.
        user = User.objects.get(email='usertest@t.fr')
        self.assertEqual(user.check_password('Deux2020'), True)

        # Apply a change.
        response = self.client.post(self.password_url, {
            "old_password": "Deux2020",
            "new_password1": "Trois2121",
            "new_password2": "Quatre2121"
        })
        # No redirection because the password change failed.
        self.assertEqual(response.status_code, 200)
