from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from shop.models import Product
from shop.utils import ProductFactory

User = get_user_model()

from faker import Faker

fake = Faker()


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=False)
        self.test_admin_user = User.objects.create(username='test_user', email='testuser@test.com',
                                                   password='rrrr', phone='+16469061833',is_staff=True,
                                                   is_superuser=True, is_active=True)

    def test_api_product_unauthenticated_can_list_published_only(self):
        ProductFactory(2, False, tags=['computers', 'phones'])
        ProductFactory(2, True, tags=['computers', 'phones'])

        response = self.client.get(reverse('api-shop:product-list'))
        for prod in response.json().get('results'):
            self.assertTrue(prod['published'])

    def test_unique_product_slugify_backend(self):
        ProductFactory(2, True, tags=['computers', 'phones'])
        products = Product.objects.all()
        product_1 = products[0]
        product_2 = products[1]
        product_1.name = 'Macbook pro'
        product_1.save()
        product_2.name = 'Macbook pro'
        product_2.save()
        self.assertEqual(product_1.slug, 'macbook-pro')
        self.assertEqual(len(product_2.slug), len(product_1.slug)+5)

    def test_api_product_user_can_retrieve(self):
        ProductFactory(2, True, tags=['computers', 'phones'])
        product = Product.objects.last()
        response = self.client.get(reverse('api-shop:product-detail', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('computers', response.json().get('tags'))

    def test_api_product_authorized_admin_can_list_all_products(self):
        for state in [True, False]:
            ProductFactory(2, state, tags=['computers', 'phones'])
        self.client.force_authenticate(self.test_admin_user)
        response = self.client.get(reverse('api-shop:product-list'))
        self.assertEqual(response.json().get('count'), 4)
        self.assertFalse(Product.objects.first().published)
        self.assertTrue(Product.objects.last().published)