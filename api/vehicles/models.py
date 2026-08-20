import uuid
from django.db import models


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vin = models.CharField('VIN', max_length=17, unique=True)
    make = models.CharField('Make', max_length=50)
    model = models.CharField('Model', max_length=50)
    year = models.PositiveIntegerField('Year')
    daily_rate = models.DecimalField('Daily Rate', max_digits=10, decimal_places=2)
    status = models.CharField(
        'Status',
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('rented', 'Rented'),
            ('maintenance', 'In Maintenance'),
            ('returned', 'Returned'),
        ],
        default='available',
    )
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        ordering = ['make', 'model']

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.vin})"

    @property
    def is_available(self):
        return self.status == 'available'