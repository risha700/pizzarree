from taggit.serializers import TaggitSerializer, TagListSerializerField
from rest_framework import serializers

from shop.models import Product


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

