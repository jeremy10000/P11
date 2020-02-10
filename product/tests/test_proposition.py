from django.test import TestCase, Client
from django.urls import reverse

from product.models import Product
from login.models import User


class PropositionViewTest(TestCase):
    """ PropositionView """
    fixtures = ["products.json"]

    def setUp(self):
        self.client = Client()

    def test_proposition_url_and_template(self):
        response = self.client.get('/product/proposition/1')
        self.assertTemplateUsed(response, 'product/proposition.html')
        self.assertEqual(response.status_code, 200)

    def test_proposition_better_nutriscore_or_equivalent_and_exclude_id(self):
        r = self.client.get('/product/proposition/1')

        self.assertEqual(r.context_data["object_list"].count(), 2)
        self.assertEqual(r.status_code, 200)

        # id=1 because self.client.get('/product/proposition/1')
        if not Product.objects.get(id=1) in r.context_data["object_list"]:
            exclude_id = True

        self.assertTrue(exclude_id)

    def test_proposition_no_products(self):
        response = self.client.get('/product/proposition/2')

        self.assertEqual(response.context_data["object_list"].count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_proposition_unknown_id(self):
        response = self.client.get('/product/proposition/90')
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200)

    def test_proposition_context_data(self):
        response = self.client.get('/product/proposition/1')
        self.assertEqual(response.status_code, 200)

        # id=1 because self.client.get('/product/proposition/1')
        product = Product.objects.get(id=1)

        self.assertEqual(response.context_data["search"], product.name)
        self.assertEqual(response.context_data["product"], product.id)
        self.assertEqual(response.context_data["photo"], product.photo)
