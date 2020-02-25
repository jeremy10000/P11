import time
import re

from django.contrib.sessions.models import Session
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from login.models import User
from product.models import Substitute
from purbeurre.settings import DEFAULT_FROM_EMAIL

# Travis.
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('window-size=1200x600')


class TestChrome(StaticLiveServerTestCase):
    """ Functionalities are tested with selenium. """
    fixtures = ["products.json"]

    def setUp(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(self.live_server_url)

    def tearDown(self):
        self.driver.close()

    def test_create_an_account(self):
        """ Create an account. """
        self.assertEqual(User.objects.all().count(), 0)

        # Click on the icon to create an account.
        self.driver.find_elements_by_tag_name('a')[2].click()
        self.assertIn("Créer un compte", self.driver.title)
        time.sleep(1)

        self.driver.find_element_by_id("id_email").send_keys("jeudi@test.fr")
        self.driver.find_element_by_id("id_password1").send_keys("samedi2020")
        self.driver.find_element_by_id("id_password2").send_keys("samedi2020")
        time.sleep(1)
        self.driver.find_element_by_id("id_password2").submit()
        time.sleep(2)
        self.assertEqual(User.objects.all().count(), 1)

    def test_change_the_username_and_password(self):
        """ Change the username and password. """
        self.user = User.objects.create(email='jeudi@test.fr')
        self.user.set_password('samedi2020')
        self.user.save()

        # Click on the icon to login.
        self.driver.find_elements_by_tag_name('a')[1].click()
        self.assertIn("Se connecter", self.driver.title)
        self.driver.find_element_by_id("id_username")\
            .send_keys("jeudi@test.fr")
        self.driver.find_element_by_id("id_password")\
            .send_keys("samedi2020")
        time.sleep(1)
        self.driver.find_element_by_id("id_password").submit()
        time.sleep(2)
        self.assertIn("Mon compte", self.driver.title)

        # Change the username.
        self.driver.find_elements_by_tag_name('button')[1].click()
        self.assertIn("Changer le profil", self.driver.title)
        self.driver.find_element_by_id("id_first_name").send_keys("Marie")
        self.driver.find_element_by_id("id_last_name").send_keys("SonNom")
        time.sleep(1)
        self.driver.find_element_by_id("id_last_name").submit()
        time.sleep(2)
        self.assertIn("Mon compte", self.driver.title)

        # Change password.
        self.driver.find_elements_by_tag_name('a')[4].click()
        self.driver.find_element_by_id("id_old_password")\
            .send_keys("samedi2020")
        self.driver.find_element_by_id("id_new_password1")\
            .send_keys("lundi1500")
        self.driver.find_element_by_id("id_new_password2")\
            .send_keys("lundi1500")
        time.sleep(1)
        self.driver.find_element_by_id("id_new_password2").submit()
        time.sleep(2)
        self.assertIn("Mot de passe modifié", self.driver.title)

    def test_forgot_your_password(self):
        """ Test the functionality: send the mail and the token. """
        self.user = User.objects.create(email='jeudi@test.fr')
        self.user.set_password('samedi2020')
        self.user.save()

        # Click on the icon to login.
        self.driver.find_elements_by_tag_name('a')[1].click()
        time.sleep(1)

        # Click on the link "Mot de passe oublié".
        self.driver.find_elements_by_tag_name('p')[0].click()
        time.sleep(1)
        self.assertIn("Mot de passe oublié", self.driver.title)
        self.driver.find_element_by_id("id_email").send_keys("jeudi@test.fr")
        time.sleep(1)
        self.driver.find_element_by_id("id_email").submit()
        time.sleep(2)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "Réinitialiser votre mot de passe")

        # Catch the link in the e-mail.
        mail_link = re.search(r'http+.+', mail.outbox[0].body).group()

        self.assertEqual(mail.outbox[0].to, ['jeudi@test.fr'])
        self.assertEqual(mail.outbox[0].from_email, DEFAULT_FROM_EMAIL)

        self.driver.get(mail_link)
        time.sleep(1)
        self.driver.find_element_by_id("id_new_password1")\
            .send_keys("Minuit14f")
        self.driver.find_element_by_id("id_new_password2")\
            .send_keys("Minuit14f")
        time.sleep(1)
        self.driver.find_element_by_id("id_new_password2").submit()
        time.sleep(2)
        self.assertIn("Mot de passe modifié", self.driver.title)

    def test_save_and_login(self):
        """
            Tests session variables to keep the user's product selection,
            if the user is not logged in.
        """
        self.user = User.objects.create(email='jeudi@test.fr')
        self.user.set_password('samedi2020')
        self.user.save()

        # Search a product.
        self.driver.find_element_by_name("query").send_keys("Mayo")
        time.sleep(1)
        self.driver.find_element_by_name("query").submit()
        time.sleep(2)

        # Select a product.
        self.assertIn("Recherche", self.driver.title)
        self.driver.find_elements_by_tag_name('a')[3].click()
        time.sleep(2)

        # Click on "Sauvegarder".
        self.assertIn("Proposition", self.driver.title)
        self.driver.find_elements_by_tag_name('button')[1].click()
        time.sleep(2)

        # No products registered.
        self.assertEqual(Substitute.objects.all().count(), 0)

        # Session variables have been created.
        cookie = self.driver.get_cookies()
        session_id = cookie[0]["value"]
        session = Session.objects.get(session_key=session_id)
        session_data = session.get_decoded()
        self.assertIn('save', session_data.keys())
        self.assertIn('save_page', session_data.keys())

        (p_id, s_id) = session_data['save']
        page = session_data['save_page']
        self.assertEqual((p_id, s_id), ('1', '2'))
        self.assertEqual(page, '/product/proposition/1')

        # Redirection to the login page. The user logs in.
        self.assertIn("Se connecter", self.driver.title)
        self.driver.find_element_by_id("id_username")\
            .send_keys("jeudi@test.fr")
        self.driver.find_element_by_id("id_password")\
            .send_keys("samedi2020")
        time.sleep(1)
        self.driver.find_element_by_id("id_password").submit()
        time.sleep(5)

        # Authentication successful. Redirection to the favorites page.
        self.assertIn("Mes favoris", self.driver.title)

        # The product is registered.
        self.assertEqual(Substitute.objects.all().count(), 1)

        # Session variables have been deleted.
        with self.assertRaises(Session.DoesNotExist):
            session = Session.objects.get(session_key=session_id)
