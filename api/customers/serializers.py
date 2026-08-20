from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'phone', 'license_number',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('Email is required.')
        return value.strip().lower()

    def validate_license_number(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('License number is required.')
        return value.strip().upper()