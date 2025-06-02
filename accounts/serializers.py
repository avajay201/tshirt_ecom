from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_password(self, value):
        if len(value.strip()) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters.")
        return value

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        first_name, *last_name = full_name.strip().split(' ')
        validated_data['first_name'] = first_name
        validated_data['last_name'] = ' '.join(last_name) if last_name else ''
        validated_data['username'] = validated_data['email'].split('@')[0]
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return {
            'status': True,
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user is None or not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("Unverified account, Please verify your account first.")

        refresh = RefreshToken.for_user(user)
        return {
            'name': user.first_name + ' ' + user.last_name,
            'email': user.email,
            'access': str(refresh.access_token),
        }
