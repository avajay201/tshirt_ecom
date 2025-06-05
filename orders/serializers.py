from rest_framework import serializers
from .models import Address
from .utils import pincode_check


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user', None)
        representation.pop('created_at', None)
        representation.pop('user', None)
        return representation

    def validate_postal_code(self, value):
        is_valid = pincode_check(value)
        if not is_valid:
            raise serializers.ValidationError("Entered pin code is invalid.")
        return value
