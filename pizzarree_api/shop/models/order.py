import uuid
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Address(models.Model):
    ADDRESS_TYPE = (
        ('BILLING', _('Billing Address')),
        ('SHIPPING', _('Shipping Address')),
    )
    address_type = models.CharField(choices=ADDRESS_TYPE, default=ADDRESS_TYPE[1], max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    address_2 = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = PhoneNumberField(null=True, blank=True)


class Order(models.Model):
    PAYMENT_OPS = (
        ('CASH', _('Cash')),
        ('ONLINE', _('Online')),
    )
    STATUS_OPTS = (
        ('PENDING', _('pending')),
        ('PROCESSING', _('processing')),
        ('SHIPPED', _('shipped')),
        ('DELIVERED', _('delivered')),
        ('CANCELLED', _('cancelled')),
        ('REFUNDED', _('refunded')),
    )
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField()
    phone = PhoneNumberField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_OPS, blank=True, null=True)
    status = models.CharField(choices=STATUS_OPTS, default=STATUS_OPTS[0], max_length=64)
    coupon = models.OneToOneField('Coupon', related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    billing_address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='billing_address')
    shipping_address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True,
                                            related_name='shipping_address')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return _('Order {}').format(self.id)

    def get_total_cost(self):
        return self.total_items_cost - self.discount_value

    @property
    def total_cost(self):
        return self.get_total_cost()

    @property
    def discount_value(self):
        value = 0
        if self.coupon:
            if self.coupon.discount_type == 'PERCENT':
                value = self.total_items_cost * (self.coupon.discount / Decimal('100'))
            else:
                value = self.coupon.discount
        return value

    @property
    def total_items_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    @property
    def shipping_cost(self):
        raise NotImplemented()

    def cancel(self):
        """
        Services has no refund
        if payment authorized and captured refund fees applies
        if order in shipped status, refund fees applies
        if return after fulfillment, cancellation fees applies.
        must calculate refund fee and shipping cost if any
        then process refund, increment stock
        """
        raise NotImplemented()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    # tax = models.DecimalField(max_digits=10, decimal_places=2) # TODO

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    COUPON_TYPES = (
        ('FIXED', _('Fixed')),
        ('PERCENT', _('Percent')),
    )
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_type = models.CharField(choices=COUPON_TYPES, max_length=255, default=COUPON_TYPES[1])
    active = models.BooleanField()
    # max_value = # TODO

    def __str__(self):
        return self.code


