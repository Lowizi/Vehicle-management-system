from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id', 'vin', 'make', 'model', 'year',
            'daily_rate', 'status', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_vin(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('VIN is required.')
        return value.strip().upper()

    def validate_year(self, value):
        current_year = 2026
        if value < 1990 or value > current_year:
            raise serializers.ValidationError(
                f'Year must be between 1990 and {current_year}.'
            )
        return value

    def validate_daily_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError('Daily rate must be positive.')
        return value