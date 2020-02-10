from django.test import TestCase, Client
from django.urls import reverse
from login.models import User


class MyPageTest(TestCase):
    """ Test user profile """

    def setUp(self):
        """ Before every test """
        self.client = Client()
        self.login_url = reverse('login:connect')
        self.mypage_url = reverse('login:mypage')
        # Create a new user.
        self.user = User.objects.create(email='user_test@django.test')
        self.user.set_password('@december2019')
        self.user.save()

    def test_mypage_if_the_user_is_not_logged_in(self):
        """ Test redirection """
        response = self.client.get(self.mypage_url)
        self.assertRedirects(
            response, '/login?next=/login/mypage/',
            status_code=302, target_status_code=301)

    def test_mypage_if_the_user_is_logged_in(self):
        response = self.client.post(self.login_url, {
            'username': 'user_test@django.test',
            'password': '@december2019'
        })
        response = self.client.get(self.mypage_url)
        self.assertTemplateUsed(response, 'registration/mypage.html')
        self.assertEqual(response.status_code, 200)
