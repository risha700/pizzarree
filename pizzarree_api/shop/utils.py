import json

import django_filters
import taggit
from django.db.models import Q
from django.utils import timezone
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from taggit.forms import TagField

from shop.models import Product, Coupon
from faker import Faker

fake = Faker()


class ProductFactory:
    def __init__(self, count_products=10, published=False, tags=[], assign_names=[]):
        for _ in range(count_products):
            p = Product.objects.create(name=fake.word(),
                                       price=fake.random_number(digits=3),
                                       description=fake.paragraph(nb_sentences=1),
                                       published=published)
            if len(tags):
                tag = fake.random_sample(elements=tags, length=2)
                for t in tag:
                    p.tags.add(t)
        if len(assign_names):
            for n in assign_names:
                Product.objects.create(name=n,
                                       price=fake.random_number(digits=3),
                                       description=fake.paragraph(nb_sentences=1), published=published)


class CouponFactory:
    def __init__(self, count_coupons=3, active=True, coupon_type=Coupon.COUPON_TYPES[1]):
        for _ in range(count_coupons):
            Coupon.objects.create(code=fake.word(), discount=fake.random_number(digits=2),
                                  valid_from=fake.date_time_this_month(tzinfo=fake.pytimezone()),
                                  valid_to=fake.future_datetime(tzinfo=fake.pytimezone()),
                                  discount_type=coupon_type, active=active)


class TagsFilter(filters.BaseFilterBackend):
    """
    Return all objects which match any of the provided tags
    """
    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.get('tags', None)
        from django.db.models import Q
        tag_filter = Q()
        if tags:
            tags = tags.split(',')
            for tag in tags:
                tag_filter |= Q(tags__name__icontains=tag)
            queryset = queryset.filter(tag_filter).distinct()
        return queryset



class ProductFilterClass(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    slug = django_filters.CharFilter(lookup_expr='icontains')


class OrderUUIDAuthedFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        identifier = request.query_params.get('identifier', None)
        order_email = request.query_params.get('order_email', None)
        if identifier:
            if request.user.is_anonymous:
                queryset = queryset.filter(identifier=identifier, email=order_email).distinct()
            else:
                queryset = queryset.filter(identifier=identifier, email=request.user.email).distinct()
        return queryset


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False