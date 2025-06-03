from rest_framework import serializers
from .models import ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message', 'submitted_at']
        read_only_fields = ['submitted_at']
