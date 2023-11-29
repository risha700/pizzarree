from importlib import import_module

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from shop.models import Product, Coupon, Order
from shop.models.cart import Cart
from shop.utils import ProductFactory, CouponFactory

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


get_cart = lambda res: Cart(res.wsgi_request)
engine = import_module(settings.SESSION_ENGINE)
session = engine.SessionStore()


class OrderTestCase(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create(username='test_user', email='testuser@test.com',
                                             password='rrrr', phone='+16469061833', is_staff=False,
                                             is_superuser=False, is_active=True)
        self.client = APIClient(enforce_csrf_checks=False)
        ProductFactory(10, False, tags=['computers', 'phones'])
        self.products = Product.objects.all()
        CouponFactory(1, active=False)
        CouponFactory(2)
        self.coupons = Coupon.objects.all()

    def tearDown(self) -> None:
        session.clear()

    def test_order_create(self):
        p = Product.objects.get(id=self.products[1].id)
        p.stock = 10
        p.save()
        self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.products[0].id}))
        self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.products[1].id}), {
            'quantity': 3
        })
        self.client.post(reverse('api-shop:cart-apply-coupon'), {'coupon_code': self.coupons.last().code})
        response = self.client.post(reverse('api-shop:order-list'), {
            'email': 'rs@test.local',
            'shipping_address': {'first_name': 'mr', 'last_name': 'risha', 'address': '99 main st',
                                 'postal_code': '12345', 'city': 'NY', 'country': 'USA', 'address_type': 'SHIPPING'}
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.last()
        self.assertEqual(order.shipping_address.last_name, 'risha')
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.items.get(product_id=self.products[1].id).quantity, 3)

        # scenario 2 order is pending payment will update in place
        self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.products[1].id}), {
            'quantity': 1, 'update': True
        })
        self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.products[7].id}))
        response = self.client.post(reverse('api-shop:order-list'), {
            'email': 'rs@test.local',
            'shipping_address': {'first_name': 'mr', 'last_name': 'r!sh@', 'address': '100 main st',
                                 'postal_code': '12345', 'city': 'NY', 'country': 'USA', 'address_type': 'SHIPPING'},
            'billing_address': {'first_name': 'mr', 'last_name': 'risha', 'address': '100 main st',
                                'postal_code': '12345', 'city': 'NY', 'country': 'USA', 'address_type': 'BILLING'}
        }, format='json')
        order.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(order.items.count(), 3)
        # self.assertEqual(order.shipping_address.address, '100 main st')
        self.assertEqual(order.shipping_address.last_name, 'r!sh@')
        self.assertEqual(order.billing_address.last_name, 'risha')

        self.assertEqual(order.items.get(product_id=self.products[1].id).quantity, 1)
        #
        # scenario 3 remove item
        self.client.post(reverse('api-shop:cart-remove', kwargs={'product_id': self.products[0].id}))
        res = self.client.post(reverse('api-shop:order-list'), {'email': 'rs@test.local'})
        order.refresh_from_db()
        with self.assertRaises(Exception):
            order.items.get(product_id=self.products[0].id)
        self.assertEqual(order.items.count(), 2)


    # def test_admins_can_view_all_orders(self):
    #     p = Product.objects.get(id=self.products[1].id)
    #     p.stock = 10
    #     p.save()
    #     session.clear()
    #     self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.products[0].id}))
    #     self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.products[1].id}), {
    #         'quantity': 3
    #     })
    #     self.client.post(reverse('api-shop:cart-apply-coupon'), {'coupon_code': self.coupons.last().code})
    #
    #     response = self.client.post(reverse('api-shop:order-list'), {
    #         'email': 'rs@test.local',
    #         'shipping_address': {'first_name': 'mr', 'last_name': 'risha', 'address': '99 main st',
    #                              'postal_code': '12345', 'city': 'NY', 'country': 'USA', 'address_type': 'SHIPPING'}
    #     }, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)