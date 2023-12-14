import stripe.error
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, NotAcceptable
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser, OR
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ModelViewSet, ViewSet

from shop.models import Product, Order, Coupon
from shop.models.cart import Cart
from shop.payment_gateway import PaymentGateway
from shop.permissions import IsAuthorized, IsOrderOwner
from shop.serializers import ProductSerializer, OrderSerializer
from shop.utils import ProductFilterClass, OrderUUIDAuthedFilter, TagsFilter, is_jsonable
from django.utils.translation import gettext_lazy as _


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,TagsFilter)
    # filterset_fields = ('slug', 'id')

    filter_class = ProductFilterClass
    # filterset_class = ProductFilterClass
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
        if self.action in ['list', 'retrieve', 'destroy', 'update', 'partial_update']:
            permissions = [OR(IsOrderOwner(), IsAuthorized())]
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

    @action(methods=['post'], detail=False, url_path='add(?:/(?P<product_id>[^/.]+))?')
    def add(self, request, product_id=None):
        cart = Cart(request)
        products = []

        if product_id is not None:
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product,
                     quantity=request.data.get('quantity', 1),
                     update_quantity=request.data.get('update', False))

            return Response({'message': _('{} added to cart').format(product.name)}, status=status.HTTP_202_ACCEPTED)

        if request.data.get('product_list', False):
            products = request.data.get('product_list', {})
            # products = request.data
            if len(request.data) == 0:
                raise NotAcceptable()
            products_db = Product.objects.all()
            if request.content_type != 'application/json':
                req_data = dict(request.data.lists()) if isinstance(products, str) else products
                products = []
                for x in req_data['product_list']:
                    products.append(json.loads(str(x).replace("'", "\"")))

            for prod in products:
                if isinstance(prod, dict):
                    pid = prod.get('id')
                    qty = prod.get('quantity', 1)
                    update = prod.get('update', False)
                elif is_jsonable(prod):
                    pid = prod[0]
                    qty = prod[1] if len(prod) > 1 else 1
                    update = prod[2] if len(prod) > 2 else False
                else:
                    raise NotAcceptable(detail='Object format unsupported {}'.format(type(prod)))

                p = products_db.filter(id=pid)
                if not p.exists():
                    raise NotFound()
                product = p.get()

                cart.add(product=product,quantity=qty, update_quantity=update)
            return Response({'message': _('Cart Updated')},status=status.HTTP_202_ACCEPTED)
        raise NotAcceptable()

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
    allow_stripe_headers = {
        'X-Frame-Options': 'ALLOW-FROM https://*.stripe.com'

    }

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
            if hasattr(e.error, 'payment_intent'):
                intent = e.error.payment_intent
            clt_secret = intent.client_secret if intent and intent.client_secret else None
            # raise NotAcceptable(detail=e.user_message, code=e.code)
            return Response(data={'error': e.user_message, 'client_secret': clt_secret},
                            headers=self.allow_stripe_headers)

        if intent.status == 'succeeded':
            Cart(request).clear()
            request.session.flush()
            # if coupon used invalidate it
            # cleanup server session

            # headers = {'X-Frame-Options': 'ALLOW-FROM https://*.stripe.com'}
            #TODO: send email to user to
        return Response(
            data={'intent_status': intent.status, 'client_secret': intent.client_secret},
            headers=self.allow_stripe_headers)
