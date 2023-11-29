from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse
from taggit.managers import TaggableManager


class Product(models.Model):
    PRODUCT_TYPES = (
        ('SALE', _('Sale')),
        ('SERVICE', _('Service')),
    )
    name = models.CharField(max_length=255, db_index=True, blank=False)
    slug = models.SlugField(max_length=255, blank=True, db_index=True, unique=True)
    type = models.CharField(choices=PRODUCT_TYPES, max_length=255, default=PRODUCT_TYPES[0])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    published = models.BooleanField(default=False, db_index=True)
    featured = models.BooleanField(default=False)
    info = models.JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    cover_image = models.ImageField(upload_to='uploads/products/', blank=True, verbose_name=_('cover_image'))

    class Meta:
        ordering = ('-created', )
        unique_together = ('name', 'slug', 'id', )

    def __str__(self):
        return ' #{} - {}'.format(self.pk, self.slug)

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self._original_slug = self.slug
        self._original_name = self.name

    def get_absolute_url(self):
        return reverse('api-store:product-detail', args=[self.pk])

    def unique_slugify(self, slug):
        used_slug = self.__class__.objects.filter(slug=slug)
        if used_slug.exists() and used_slug.get().id != self.pk:
            return '{}_{}'.format(slug, get_random_string(length=4))
        return slug

    def save(self, *args, **kwargs):
        self.slug = self.unique_slugify(slugify(self.name))
        super(Product, self).save(*args, **kwargs)

    @property
    def object_has_changed(self):
        return (self._original_slug is not None and self._original_slug != self.slug) \
               or (self._original_name is not None and self._original_name != self.name)
