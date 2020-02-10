from django.test import TestCase, Client
from django.urls import reverse

from login.models import User


class SearchViewTest(TestCase):
    """ SearchView """
    fixtures = ["products.json"]

    def setUp(self):
        self.client = Client()
        self.search_url = reverse('product:search')

    def test_search_url_and_template(self):
        response = self.client.get(self.search_url + "?query=TEST")
        self.assertTemplateUsed(response, 'product/search.html')
        self.assertEqual(response.status_code, 200)

    def test_search_url_404(self):
        response = self.client.get(self.search_url + "?query=Mayo&page=@")
        self.assertEqual(response.status_code, 404)

    def test_search_no_query(self):
        response = self.client.get(self.search_url)
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200)

    def test_search_context_search(self):
        response = self.client.get(self.search_url + "?query=Beurre")
        self.assertEqual(response.context_data["search"], "Beurre")

    def test_search_product_found(self):
        response = self.client.get(self.search_url + "?query=mayo")
        self.assertEqual(response.context_data["object_list"].count(), 1)

    def test_search_zero_product(self):
        response = self.client.get(self.search_url + "?query=moutarde")
        self.assertEqual(response.context_data["object_list"].count(), 0)
