from django.test import Client, TransactionTestCase
from django.db import IntegrityError

from product.models import Category, Level, Product, Substitute
from login.models import User

from unittest.mock import patch
from django.core.management import call_command


class BaseCommandsTest(TransactionTestCase):
    """ Test BaseCommand """
    fixtures = ["products.json"]

    @patch("product.management.commands.add-level.STDOUT", new_callable=bool)
    def test_add_level_errors(self, mock):
        # Don't display messages.
        mock = False

        with self.assertRaises(TypeError):
            call_command("add-level", level=10)

        with self.assertRaises(TypeError):
            call_command("add-level")

    @patch("product.management.commands.add-level.STDOUT", new_callable=bool)
    def test_add_level_success_and_integrity_error(self, mock):
        # Don't display messages.
        mock = False

        self.assertEqual(Level.objects.all().count(), 3)

        call_command("add-level", level="Very Low")
        self.assertEqual(Level.objects.all().count(), 4)
        # Duplicate is not allowed.
        call_command("add-level", level="Very Low")
        self.assertEqual(Level.objects.all().count(), 4)

    @patch("product.management.commands.add-product.STDOUT", new_callable=bool)
    def test_add_product_errors(self, mock):
        # Don't display messages.
        mock = False

        with self.assertRaises(TypeError):
            call_command("add-product", nutriscore="o")

        with self.assertRaises(TypeError):
            call_command("add-product", category=12)

    @patch("product.management.commands.add-product.requests.get")
    @patch("product.management.commands.add-product.STDOUT", new_callable=bool)
    def test_add_product_success_and_error(self, mock, mock_json):
        # Don't display messages.
        mock = False

        mock_json.return_value.json.return_value = {
            'products': [{
                'nutrient_levels': {
                    'sugars': 'low',
                    'salt': 'low',
                    'fat': 'high',
                    'saturated-fat': 'moderate',
                },
                'nutriments': {
                    'salt_100g': '1.1',
                    'sugars_100g': '1.09',
                    'fat_100g': '22.15',
                    'saturated-fat_100g': '10.2',
                },
                'image_url': 'https://image.fr',
                'nutrition_grade_fr': ['a'],
                'url': 'https://url.fr',
                'product_name_fr': 'Nom du Produit Mock', },

                {
                'nutrient_levels': {
                    'sugars': 'low',
                    'salt': 'low',
                    'fat': 'high',
                    'saturated-fat': 'moderate',
                },
                'nutriments': {
                    'salt_100g': '1.1',
                    'sugars_100g': '1.09',
                    'fat_100g': '22.15',
                    'saturated-fat_100g': '10.2',
                },
                'image_url': 'https://image2.fr',
                'nutrition_grade_fr': ['a'],
                'url': 'https://url2.fr',
                'product_name_fr': 'Nom du Produit Mock 2',
            }]
        }

        self.assertEqual(Product.objects.all().count(), 3)
        self.assertEqual(Category.objects.all().count(), 1)
        # Add a category and products.
        call_command("add-product", nutriscore="a", category="Desserts")
        self.assertEqual(Product.objects.all().count(), 5)
        self.assertEqual(Category.objects.all().count(), 2)
        # Duplicate is not allowed.
        call_command("add-product", nutriscore="a", category="Desserts")
        self.assertEqual(Product.objects.all().count(), 5)
        self.assertEqual(Category.objects.all().count(), 2)
