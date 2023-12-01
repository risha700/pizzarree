

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from shop.models import Order


User = get_user_model()


class UserVault(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    vault_id = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return _('User {}#{}').format(self.user.username, self.vault_id)

    def __str__(self):
        return _('User {}#{}').format(self.user.username, self.vault_id)


class PaymentLog(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=128)
    info = models.JSONField(default=dict, null=True, blank=True)

    def __unicode__(self):
        return '%s charged %s - #%s' % (self.user or 'Guest', self.amount, self.transaction_id)

    def __str__(self):
        return '%s charged %s - #%s' % (self.user or 'Guest', self.amount, self.transaction_id)
