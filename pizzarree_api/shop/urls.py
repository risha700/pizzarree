from django.urls import include, re_path

from .views import ProductViewSet
# OrderViewSet, CartViewSet, PaymentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
# router.register(r'orders', OrderViewSet, basename='order')
# router.register(r'cart', CartViewSet, basename='cart')
# router.register(r'payment', PaymentViewSet, basename='payment')
#
urlpatterns = router.urls
