from importlib import import_module

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APIRequestFactory

from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APITestCase
from django.test import override_settings

from shop.models import Product, Coupon, Order,PaymentLog
from shop.models.cart import Cart
from shop.payment_gateway import PaymentGateway
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

    def test_api_filter_products_by_pk_and_slug(self):
        ProductFactory(10, True, tags=['computers', 'phones', 'IOS', 'Android'], assign_names=['macbook pro'])
        response = self.client.get(reverse('api-shop:product-list'),  {'tags': 'ios,android'})
        # print(response.content)
        self.assertIn('IOS', response.json().get('results')[0].get('tags'))
        response = self.client.get(reverse('api-shop:product-list'),  {'name': 'macbook pro'})
        self.assertIn('macbook pro', response.json().get('results')[0].get('name'))
        response = self.client.get(reverse('api-shop:product-list'),  {'slug': 'macbook-pro'})
        self.assertIn('macbook-pro', response.json().get('results')[0].get('slug'))

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


class CartTestCase(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create(username='test_user', email='testuser@test.com',
                                             password='rrrr', phone='+16469061833', is_staff=False,
                                             is_superuser=False, is_active=True)
        self.client = APIClient(enforce_csrf_checks=False)
        ProductFactory(3, False, tags=['computers', 'phones'])
        self.product = Product.objects.last()
        self.product_2 = Product.objects.first()
        CouponFactory(1, active=False)
        CouponFactory(2)
        self.coupons = Coupon.objects.all()
        self.product_2.stock = 3
        self.product_2.save()
        self.product.stock = 3
        self.product.save()

    def tearDown(self) -> None:
        session.clear()
    def test_add_product_to_cart(self):
        # add product to cart
        response = self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.json()['message'], '{} added to cart'.format(self.product.name))
        self.assertEqual(get_cart(response).cart, self.client.session[settings.CART_SESSION_ID])
        # add product-2
        response_2 = self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.product_2.id}))
        self.assertEqual(response_2.json()['message'], '{} added to cart'.format(self.product_2.name))
        self.assertEqual(get_cart(response_2).cart, self.client.session[settings.CART_SESSION_ID])
        self.assertEqual(len(get_cart(response_2).cart), 2)

        # added more products
        add_more_response = self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.product.id}),
                                             {'quantity': 2})
        self.assertEqual(get_cart(add_more_response).cart.get(str(self.product.id)).get('quantity'), 3)

    def test_add_many_products_to_cart(self):
        self.product.stock = 10
        self.product_2.stock = 10
        self.product.save()
        self.product_2.save()
        # add products to cart
        response = self.client.post(reverse('api-shop:cart-add'),data={
                "product_list": [
                        [self.product.id, 2, "True"], [self.product_2.id, 1]
                ]
        }, format='json')
        # print(response.content)
        self.assertEqual(response.json()['message'], 'Cart Updated')
        self.assertEqual(get_cart(response).cart, self.client.session[settings.CART_SESSION_ID])
        self.assertEqual(len(get_cart(response).cart), 2)

        bad_response = self.client.post(reverse('api-shop:cart-add'),data={
                "product_list": [
                        [277, 200, "True"], [self.product_2.id, 1]
                ]
        }, format='json')
        self.assertEqual(bad_response.json().get('detail'), 'Not found.' )


        # test without json
        response = self.client.post(reverse('api-shop:cart-add'),data={
                "product_list": [
                        [self.product.id, 2, "True"], [self.product_2.id, 1]
                ]
        })
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
     # test with complex object
        response = self.client.post(reverse('api-shop:cart-add'),data={
                "product_list": [
                    {
                        "id":self.product.id,
                        "quantity":2,
                        "update":"False"
                    },
                    {
                        "id": self.product_2.id,
                        "quantity": 1,
                    },

                ]
        })
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
    def test_update_qty(self):
        # update qty
        update_qty_response = self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.product_2.id}),
                                               {'quantity': 3, 'update': True})
        self.assertEqual(int(get_cart(update_qty_response).cart.get(str(self.product_2.id)).get('quantity')), 3)

    def test_cart_detail(self):
        # cart detail
        detail_response = self.client.get(reverse('api-shop:cart-details'))
        self.assertEqual(detail_response.status_code, 200)
        # print(get_cart(detail_response).get_total_price())

    def test_cart_remove(self):
        # remove product
        remove_response = self.client.post(reverse('api-shop:cart-remove', kwargs={'product_id': self.product.id}))
        self.assertEqual(remove_response.json()['message'], '{} removed from cart'.format(self.product.name))
        self.assertEqual(get_cart(remove_response).cart, self.client.session[settings.CART_SESSION_ID])

    def test_add_product_out_of_stock_fails(self):
        out_of_stock_res = self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.product.id}),
                                            {'quantity': 10})
        self.assertEqual(out_of_stock_res.json()['detail'], 'product is out of stock')

    def test_apply_valid_coupon(self):
        response = self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.product.id}))
        self.assertIsNone(get_cart(response).coupon_id)
        coupon = self.coupons.last()
        self.assertTrue(coupon.active)
        coupon_apply_res = self.client.post(reverse('api-shop:cart-apply-coupon'), {
            'coupon_code': coupon.code
        })
        self.assertEqual(coupon_apply_res.json()['message'], 'Coupon applied')
        self.assertEqual(get_cart(coupon_apply_res).coupon_id, coupon.id)

    def test_apply_invalid_coupon(self):
        response = self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.product.id}))
        self.assertIsNone(get_cart(response).coupon_id)
        coupon = self.coupons.first()
        coupon_apply_res = self.client.post(reverse('api-shop:cart-apply-coupon'), {
            'coupon_code': coupon.code
        })
        self.assertEqual(coupon_apply_res.json()['message'], 'Coupon invalid')
        self.assertIsNone(get_cart(response).coupon_id)

payment_gw = PaymentGateway()
from .views import PaymentViewSet

class PaymentTestCase(APITestCase):
    @override_settings(ROOT_URLCONF='app.tenant_urls')
    def setUp(self) -> None:
        self.test_user = User.objects.create(username='test_user', email='testuser@test.com',
                                             password='rrrr', phone='+16469061833', is_staff=False,
                                             is_superuser=False, is_active=True)
        self.client = APIClient(enforce_csrf_checks=False)
        self.request = APIRequestFactory()
        ProductFactory(10, False, tags=['computers', 'phones'])
        self.products = Product.objects.all()
        self.successful_nonce = 'fake-valid-nonce'
        self.failed_nonce = 'fake-processor-declined-visa-nonce'
        self.visa_card = '4500600000000061'

    def tearDown(self) -> None:
        super(PaymentTestCase, self).tearDown()

    def create_order(self):
        p = Product.objects.get(id=self.products[1].id)
        p.stock = 10
        p.save()
        self.client.post(reverse('api-shop:cart-add', kwargs={'product_id': self.products[0].id}),format='json')
        order_res = self.client.post(reverse('api-shop:order-list'),
                                     data={
                                         'email': 'rs@test.local',
                                         'shipping_address': {'first_name': 'mr', 'last_name': 'risha',
                                                              'address': '99 main st', 'postal_code': '12345',
                                                              'city': 'NY', 'country': 'USA',
                                                              'address_type': 'SHIPPING'},
                                     },
                                     format='json')
        return order_res

    def test_checkout_guest(self):
        order_res = self.create_order()
        self.assertEqual(order_res.status_code, status.HTTP_201_CREATED)
        checkout_response = self.client.post(reverse('api-shop:payment-checkout', kwargs={'order_id': order_res.data.get('id')}),
                                        data={'paymentMethodId': 'pm_card_visa'})
        self.assertEqual(checkout_response.json().get('intent_status'), 'succeeded')
        self.assertIsNotNone(checkout_response.json().get('client_secret'))
        order = Order.objects.prefetch_related().get(id=order_res.data.get('id'))
        self.assertEquals(order.status, "('COMPLETED', 'completed')")
        self.assertTrue(order.paid)
        self.assertEqual(get_cart(checkout_response).cart, {})

        payment_log = PaymentLog.objects.last()
        self.assertIsNotNone(payment_log.transaction_id)
        self.assertEqual(payment_log.order.id, order_res.data.get('id'))
        self.assertTrue(payment_log.order.paid)


    def test_checkout_auth_user(self):
        order_res = self.create_order()
        self.assertEqual(order_res.status_code, status.HTTP_201_CREATED)
        self.client.force_authenticate(self.test_user)

        failed_checkout_response = self.client.post(reverse('api-shop:payment-checkout', kwargs={'order_id': order_res.data.get('id')}),
                                             data={'paymentMethodId': 'pm_card_visa_chargeDeclined'})

        self.assertEqual(failed_checkout_response.json().get('intent_status'), 'Your card was declined.')

        checkout_response = self.client.post(reverse('api-shop:payment-checkout', kwargs={'order_id': order_res.data.get('id')}),
                                             data={'paymentMethodId': 'pm_card_visa'})
        self.assertEqual(checkout_response.json().get('intent_status'), 'succeeded')

        payment_log = PaymentLog.objects.last()
        self.assertIsNotNone(payment_log.transaction_id)
        self.assertEqual(payment_log.order.id, order_res.data.get('id'))
        self.assertTrue(payment_log.order.paid)
        self.assertTrue(payment_log.user.id, self.test_user.id)
