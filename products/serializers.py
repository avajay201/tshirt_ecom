from rest_framework import serializers
from .models import Product, ProductVariant, ProductVariantImage


class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = ['image', 'alt_text']

class ProductVariantSerializer(serializers.ModelSerializer):
    images = ProductVariantImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color_name', 'color_code', 'gender', 'age_group', 'price', 'images']

class ProductSerializer(serializers.ModelSerializer):
    variant = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'tags', 'base_price', 'variant']

    def get_variant(self, obj):
        variant = obj.variants.first()
        if variant:
            return ProductVariantSerializer(variant).data
        return None
