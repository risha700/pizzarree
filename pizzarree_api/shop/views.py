import stripe.error
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser, OR
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from shop.models import Product, Order, Coupon
from shop.models.cart import Cart
from shop.payment_gateway import PaymentGateway
from shop.permissions import IsAuthorized, IsOrderOwner
from shop.serializers import ProductSerializer, OrderSerializer
from shop.utils import ProductFilterClass, OrderUUIDAuthedFilter
from django.utils.translation import gettext_lazy as _


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
            permissions = [IsAdminUser()]
        return permissions


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related('shipping_address', 'billing_address', 'coupon')
    permission_classes = [IsAuthorized]
    filter_backends = [OrderUUIDAuthedFilter]

    def get_permissions(self):
        permissions = super(OrderViewSet, self).get_permissions()
        if self.action in ['list', 'retrieve', 'destroy', 'update']:
            permissions = [OR(IsAuthorized, IsOrderOwner)]
        if self.action in ['create']:
            permissions = [AllowAny()]
        return permissions

    def create(self, request, *args, **kwargs):
        # update if exists in session
        order_session_id = request.session.get('order_id', False)
        if order_session_id:
            instance = Order.objects.get(id=order_session_id)
            serializer = self.serializer_class(instance=instance, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return super(OrderViewSet, self).create(request, *args, **kwargs)

    @action(methods=['post'], detail=False, url_path='cancel/(?P<order_id>[^/.]+)')
    def cancel(self, request, order_id=None):
        raise NotImplemented()

    @action(methods=['post'], detail=False, url_path='returns/(?P<order_id>[^/.]+)')
    def returns(self, request, order_id=None):
        raise NotImplemented()


class CartViewSet(ViewSet):
    permission_classes = [AllowAny]  # guarded by session separation

    @action(methods=['post'], detail=False, url_path='add/(?P<product_id>[^/.]+)')
    def add(self, request, product_id=None):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = request.data.get('quantity') or int(1)
        update = request.data.get('update') or False
        cart.add(product=product, quantity=quantity, update_quantity=update)
        return Response({'message': _('{} added to cart').format(product.name)}, status=status.HTTP_202_ACCEPTED)

    @action(methods=['post'], detail=False, url_path='remove/(?P<product_id>[^/.]+)')
    def remove(self, request, product_id=None):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return Response({'message': _('{} removed from cart').format(product.name)}, status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=False)
    def details(self, request):
        cart = Cart(request)
        return Response({'cart': cart.serialized_data}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def clear(self, request):
        cart = Cart(request)
        cart.clear()
        return Response({'message': _('Cart cleared')}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def apply_coupon(self, request):
        now = timezone.now()
        code = request.data.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
            return Response({'message': _('Coupon applied')}, status=status.HTTP_202_ACCEPTED)
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            return Response({'message': _('Coupon invalid')}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PaymentViewSet(PaymentGateway, ViewSet):
    permission_classes = [IsAdminUser]

    # TODO: refactor to limit perm class hasActiveCart
    @action(methods=['post'], detail=False,
            url_path='checkout/(?P<order_id>[^/.]+)', permission_classes=[AllowAny])
    def checkout(self, request, order_id=None):
        order = Order.objects.get(id=order_id)
        intent = {}
        try:
            # confirmed intent
            intent = self.process_payment(request, order)
        except stripe.error.StripeError as e:
            intent = e.error.payment_intent
            return Response(data={'intent_status': e.user_message, 'client_secret': intent.client_secret})

        if intent.status == 'succeeded':
            Cart(request).clear()

        return Response(data={'intent_status': intent.status, 'client_secret': intent.client_secret})
