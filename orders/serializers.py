from rest_framework import serializers
from .models import Address, Order
from .utils import pincode_check
from datetime import datetime
from django.conf import settings


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('created_at', None)
        representation.pop('user', None)
        representation.pop('is_default', None)
        return representation

    def validate_postal_code(self, value):
        is_valid = pincode_check(value)
        if not is_valid:
            raise serializers.ValidationError("Entered pin code is invalid.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('id', 'user', 'shipping_address')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = datetime.strftime(instance.created_at, '%b %m, %Y')
        products = []
        for item in instance.items.all():
            products.append(
                {
                    "name": item.name,
                    "size": item.size,
                    "color": item.color,
                    "quantity": item.quantity,
                    "price": item.price,
                    "image": settings.BASE_URL + item.image.url if item.image else None,
                }
            )
        representation['products'] = products
        return representation
