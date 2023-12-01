import django.dispatch
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from shop.models import OrderItem, Order, STATUS_OPTS
from shop.payment_gateway import payment_received

from django.utils.translation import gettext_lazy as _


@receiver(post_save, sender=OrderItem)
def adjust_product_stock(sender, instance, created, **kwargs):
    """TODO"""


@receiver(payment_received)
def announce_payment_received(sender, **kwargs):
    transaction = kwargs.get('transaction', {})
    order = kwargs.get('order', False)
    order.paid = transaction.status == 'succeeded'
    index = lambda search_term: next(i for i, (s, _) in enumerate(STATUS_OPTS) if s == search_term)
    order.status = STATUS_OPTS[index('COMPLETED')] if transaction.status == 'succeeded' else \
        STATUS_OPTS[index('PENDING')]
    order.save()

