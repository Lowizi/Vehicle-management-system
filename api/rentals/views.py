from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Rental
from .serializers import RentalSerializer
from api.responses import ResponseSerializer


@extend_schema(tags=['Rental'])
class RentalViewSet(viewsets.ViewSet):
    pagination_class = None

    def list(self, request, *args, **kwargs):
        customer_id = request.query_params.get('customer_id')
        queryset = Rental.objects.all()
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)

        serializer = RentalSerializer(queryset, many=True)
        return ResponseSerializer.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = RentalSerializer(data=request.data)
        if serializer.is_valid():
            rental = serializer.save()
            return ResponseSerializer.success(
                data=RentalSerializer(rental).data,
                message='Rental created successfully.',
                status=status.HTTP_201_CREATED
            )
        return ResponseSerializer.error(
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )