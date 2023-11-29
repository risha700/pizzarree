from copy import copy
from decimal import Decimal
from django.conf import settings
from rest_framework.exceptions import NotAcceptable

from shop.models import Product, Coupon


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = self.__serialize_product__(product)
            # self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = float(item['price']) * float(item['quantity'])
            yield item

    @staticmethod
    def __serialize_product__(val):
        from shop.serializers import CartProductSerializer
        serialized = CartProductSerializer(val)
        return serialized.data

    @property
    def serialized_data(self):
        data = []
        for item in self:
            # item['product'] = self.__serialize_product__(item['product'])
            data.append(item)
        return data

    def verify_stock_level(self, product,req_quantity):
        if int(req_quantity) > int(product.stock):
            raise NotAcceptable(detail='product is out of stock', code='out_of_stock')

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        self.verify_stock_level(product, quantity)
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        else:
            real_qty = int(quantity) + int(self.cart[str(product.id)].get('quantity',0))
            self.verify_stock_level(product, real_qty)
            if update_quantity:
                real_qty = quantity
            self.cart[product_id]['quantity'] = int(real_qty)
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_discount(self):
        if self.coupon:
            if self.coupon.discount_type == 'PERCENT':
                return (self.coupon.discount / Decimal('100')) * self.get_total_price()
            else:
                return self.coupon.discount
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
