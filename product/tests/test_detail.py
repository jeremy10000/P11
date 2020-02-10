from django.test import TestCase, Client


class DetailViewTest(TestCase):
    """ DetailView """
    fixtures = ["products.json"]

    def setUp(self):
        self.client = Client()

    def test_detail_url_template_and_valid_id(self):
        response = self.client.get('/product/detail/1')
        self.assertTemplateUsed(response, 'product/detail.html')
        self.assertEqual(response.status_code, 200)

    def test_detail_invalid_id(self):
        response = self.client.get('/product/detail/90')
        self.assertEqual(response.status_code, 404)
