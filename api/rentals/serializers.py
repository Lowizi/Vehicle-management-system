from rest_framework import serializers
from .models import Rental
from .models import Vehicle
from api.customers.models import Customer


class RentalSerializer(serializers.ModelSerializer):
    vehicle_details = serializers.CharField(source='vehicle.vin', read_only=True)
    customer_details = serializers.CharField(source='customer.name', read_only=True)
    vehicle_id = serializers.CharField(write_only=True)
    customer_id = serializers.CharField(write_only=True)

    class Meta:
        model = Rental
        fields = [
            'id', 'vehicle', 'vehicle_id', 'customer', 'customer_id',
            'rental_date', 'expected_return_date', 'actual_return_date',
            'total_charge', 'status', 'created_at', 'updated_at',
            'vehicle_details', 'customer_details',
        ]
        read_only_fields = [
            'id', 'rental_date', 'created_at', 'updated_at',
            'vehicle_details', 'customer_details',
        ]
        extra_kwargs = {
            'vehicle': {'required': False},
            'customer': {'required': False},
        }

    def validate(self, data):
        vehicle_id = data.get('vehicle_id')
        customer_id = data.get('customer_id')

        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
                if vehicle.status != 'available':
                    raise serializers.ValidationError(
                        f'Vehicle {vehicle.vin} is not available (status: {vehicle.status}).'
                    )
                data['vehicle'] = vehicle
            except Vehicle.DoesNotExist:
                raise serializers.ValidationError(f'Vehicle ID {vehicle_id} not found.')

        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
                data['customer'] = customer
            except Customer.DoesNotExist:
                raise serializers.ValidationError(f'Customer ID {customer_id} not found.')

        return data

    def create(self, validated_data):
        vehicle = validated_data['vehicle']
        customer = validated_data['customer']
        vehicle.status = 'rented'
        vehicle.save()

        rental = Rental.objects.create(
            vehicle=vehicle,
            customer=customer,
            expected_return_date=validated_data.get('expected_return_date'),
        )
        return rental