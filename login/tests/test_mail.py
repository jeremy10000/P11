from django.test import TestCase
from django.core import mail
from purbeurre.settings import DEFAULT_FROM_EMAIL


class MailTest(TestCase):
    """ Test: send an email. """

    def test_send_mail(self):
        mail.send_mail(
                'Objet du mail',
                'Le message',
                'test@mail.fr',
                [DEFAULT_FROM_EMAIL]
            )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Objet du mail')
        self.assertEqual(mail.outbox[0].body, 'Le message')
        self.assertEqual(mail.outbox[0].from_email, 'test@mail.fr')
        self.assertEqual(mail.outbox[0].to,
                         ['Pur Beurre <support@purbeurre.fr>'])
