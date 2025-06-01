from rest_framework import serializers
from .models import Product, ProductVariant, ProductVariantImage
from django.conf import settings
from django.db.models import Avg
from rest_framework.exceptions import ValidationError


class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = ['image', 'alt_text']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = settings.BASE_URL + representation['image'] if representation['image'] else None
        return representation

class ProductVariantSerializer(serializers.ModelSerializer):
    images = ProductVariantImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color_name', 'color_code', 'gender', 'age_group', 'price', 'images']

# class ProductsSerializer(serializers.ModelSerializer):
#     variant = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'tags', 'base_price', 'variant']

#     def get_variant(self, obj):
#         variant = obj.variants.first()
#         if variant:
#             return ProductVariantSerializer(variant).data
#         return None

class ProductReviews(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['rating', 'comment', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.user.first_name + instance.user.last_name if instance.user else 'Anonymous'
        return representation

class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description']

    def to_representation(self, instance):
        # Filter variants by color and size if provided
        color = None
        size = None
        
        try:
            request = self.context.get('request')
            color = request.query_params.get('color')
            size = request.query_params.get('size')
        except AttributeError:
            pass

        variants_qs = instance.variants.all()
        if color:
            variants_qs = variants_qs.filter(color_name=color)
        if size:
            variants_qs = variants_qs.filter(size=size)

        if not variants_qs.exists():
            raise ValidationError("Selected variant is currently unavailable.")

        variant = variants_qs.first() or instance.variants.first()

        representation = super().to_representation(instance)

        representation['price'] = variant.price
        representation['stock'] = variant.stock

        all_variants = instance.variants.all()
        colors_qs = all_variants.values_list('color_name', 'color_code').distinct()
        representation['colors'] = [{'name': name, 'value': value} for name, value in colors_qs]
        representation['sizes'] = list(all_variants.values_list('size', flat=True).distinct())

        representation['images'] = ProductVariantImageSerializer(variant.images.all(), many=True).data
        representation['features'] = []
        representation['reviews'] = ProductReviews(instance.reviews.all().order_by('-created_at'), many=True).data
        representation['average_rating'] = instance.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        return representation
