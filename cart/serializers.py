from rest_framework import serializers
from .models import CartItem
from django.conf import settings


class CartItemSerializer(serializers.ModelSerializer):
    variant = serializers.PrimaryKeyRelatedField(source='variant.id', read_only=True)
    product = serializers.PrimaryKeyRelatedField(source='variant.product.id', read_only=True)
    name = serializers.CharField(source='variant.product.name', read_only=True)
    size = serializers.CharField(source='variant.size', read_only=True)
    color = serializers.CharField(source='variant.color_name', read_only=True)
    stock = serializers.IntegerField(source='variant.stock', read_only=True)
    price = serializers.IntegerField(source='get_total_price', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'product', 'quantity', 'price', 'name', 'size', 'color', 'stock']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        varaint_image = instance.variant.images.first()
        representation['image'] = settings.BASE_URL + varaint_image.image.url if varaint_image.image else None
        return representation
