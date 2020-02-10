from django.test import TestCase, Client
from django.urls import reverse
from login.models import User


class LoginTest(TestCase):
    """ Test Login """

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login:connect')
        self.logout_url = reverse('login:disconnect')
        # Create a new user.
        self.user = User.objects.create(email='user_test@django.test')
        self.user.set_password('@december2019')
        self.user.save()

    def test_login_url_and_template(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.status_code, 200)

    def test_login_valid(self):
        """
            - Login : username, password (ok)
            - redirection to /login/mypage/
        """
        response = self.client.post(self.login_url, {
            'username': 'user_test@django.test',
            'password': '@december2019'
        })
        self.assertRedirects(
            response, '/login/mypage/',
            status_code=302, target_status_code=200)

    def test_login_invalid(self):
        """
            - Login : username, password (not ok)
            - no redirection
        """
        response = self.client.post(self.login_url, {
            'username': 'user_test@django.test',
            'password': '@december'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(self.logout_url)
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200)
