from django.db import transaction
from taggit.serializers import TaggitSerializer, TagListSerializerField
from rest_framework import serializers

from shop.models import Product, Address, OrderItem, Order
from shop.models.cart import Cart


class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('slug', 'created', 'updated',)

    def create(self, validated_data):
        instance = super(ProductSerializer, self).create(validated_data)
        return instance

    def update(self, instance, validated_data):
        return super(ProductSerializer, self).update(instance, validated_data)


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'slug', 'name', 'cover_image', 'stock', 'price', )


class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    product = CartProductSerializer()

    class Meta:
        model = OrderItem
        exclude = ()


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    billing_address = AddressSerializer(required=False)
    shipping_address = AddressSerializer(required=False)
    identifier = serializers.UUIDField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'email', 'phone', 'updated', 'created', 'total_cost', 'paid', 'discount_value', 'coupon',
                  'items', 'status', 'payment_method', 'identifier', 'billing_address', 'shipping_address', )

    def create(self, validated_data):
        validated_data['shipping_address'] = self._create_nested_address(validated_data, address_type='shipping_address')
        validated_data['billing_address'] = self._create_nested_address(validated_data, address_type='billing_address')
        instance = super(OrderSerializer, self).create(validated_data)

        request = self._update_nested_order_items(instance)

        # don't clear it until order is officially placed
        # cart_obj.clear()
        request.session['order_id'] = instance.id
        request.session.modified = True
        # print('expiry age', request.session.get_expiry_age())  # 14 days
        return instance

    def update(self, instance, validated_data):
        for address_type in ['shipping_address', 'billing_address']:
            self._update_nested_address(instance, validated_data, address_type=address_type)
        instance.items.filter().delete()
        self._update_nested_order_items(instance)
        return super(OrderSerializer, self).update(instance, validated_data)

    def _update_nested_order_items(self, instance):
        request = self.context.get("request")
        cart_obj = Cart(request)
        if cart_obj.coupon:
            instance.coupon = cart_obj.coupon
            instance.save()
        with transaction.atomic():
            for item in cart_obj:
                if instance.items.filter(product_id=item['product'].get('id')).exists():
                    OrderItem.objects.update(order=instance, product_id=item['product'].get('id'),
                                             price=item['price'], quantity=item['quantity'])
                else:
                    OrderItem.objects.create(order=instance, product_id=item['product'].get('id'),
                                             price=item['price'], quantity=item['quantity'])
        return request

    @staticmethod
    def _create_nested_address(validated_data, address_type=None):
        address_data = validated_data.pop(address_type, False)
        if address_data:
            address_data['address_type'] = address_type
            address_instance = Address.objects.create(**address_data)
            return address_instance
        return None

    @staticmethod
    def _update_nested_address(instance, validated_data, address_type=None):
        address_data = validated_data.pop(address_type, False)
        if address_data:
            address_data['address_type'] = address_type
            address_instance = getattr(instance, address_type)
            if address_instance is not None:
                address_instance.__class__.objects.update(**address_data)
                return
            address_obj = Address.objects.create(**address_data)
            setattr(instance, address_type, address_obj)

