import datetime

from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse


# Create your models here.
class User(AbstractUser):
    """"""
    phone = PhoneNumberField(unique=True, help_text=_('Mobile number'))
    email = models.EmailField(_("Email Address"), unique=True, db_index=True, error_messages={
        'required': _("Email field is required")
        }
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'required': _("Username field is required."),
            'unique': _("A user with that username already exists."),
            'blank': _("Username field is required.")
        },

    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._original_phone = self.phone
        self._original_email = self.email

    class Meta:
        unique_together = ['email', 'phone']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return reverse('api-auth:profile', args=[self.username])

    def save(self, *args, **kwargs):
        self.check_verified_fields()
        super(User, self).save(*args, **kwargs)

    def check_verified_fields(self):
        if hasattr(self, 'profile'):
            if self._original_phone is not None:
                if self.phone != self._original_phone:
                    self.profile.phone_verified = False
            if self._original_email is not None:
                if self.email != self._original_email:
                    self.profile.email_verified = False
                self.profile.save()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('date of birth'))
    photo = models.ImageField(upload_to='uploads/users/avatar/', blank=True, verbose_name=_('photo'))
    email_verified = models.BooleanField(default=False, verbose_name=_('email verified'))
    phone_verified = models.BooleanField(default=False, verbose_name=_('phone verified'))
    temp_token = models.JSONField(blank=True, default=dict, null=True, verbose_name=_('temp token'))
    preference = models.JSONField(blank=True, default=dict, null=True, verbose_name=_('preference'))

    def __str__(self):
        return _('{} user profile').format(self.user.username)

    def save(self, **kwargs):
        self.provide_token_expiry()
        super(Profile, self).save(kwargs)

    def provide_token_expiry(self):
        token_value = self.temp_token.get('value', False)
        if token_value:
            self.temp_token['expiry'] = str(timezone.now() + datetime.timedelta(minutes=5))

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')