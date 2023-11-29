from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from shop.models import Product
from shop.serializers import ProductSerializer
from shop.utils import ProductFilterClass


# Create your views here.
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilterClass
    
    def get_queryset(self):
        qs = Product.objects.prefetch_related('tags')
        if self.request.user.is_authenticated and\
                (self.request.user.is_staff or self.request.user.is_superuser):
            return qs
        return qs.filter(published=True)

    def get_permissions(self):
        permissions = super(ProductViewSet, self).get_permissions()
        if self.action in ['list', 'retrieve']:
            permissions = [AllowAny()]
        if self.action in ['create', 'destroy', 'update']:
            # self.queryset = Product.objects.filter().select_related('cover_image').prefetch_related('media', 'tags')
            permissions = [IsAdminUser]
        return permissions
