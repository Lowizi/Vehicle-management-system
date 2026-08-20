import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from api.vehicles.models import Vehicle
from api.customers.models import Customer


def update_vehicle_rental_status(vehicle, status_val):
    """Helper to update vehicle rental status."""
    vehicle.status = status_val
    vehicle.save(update_fields=['status'])


class Rental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        verbose_name='Vehicle',
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='Customer',
    )
    rental_date = models.DateTimeField('Rental Date', auto_now_add=True)
    expected_return_date = models.DateTimeField(
        'Expected Return Date',
    )
    actual_return_date = models.DateTimeField(
        'Actual Return Date',
        null=True,
        blank=True,
    )
    total_charge = models.DecimalField(
        'Total Charge',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('returned', 'Returned'),
            ('cancelled', 'Cancelled'),
        ],
        default='active',
    )
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

    class Meta:
        verbose_name = 'Rental'
        verbose_name_plural = 'Rentals'
        ordering = ['-rental_date']

    def __str__(self):
        return f"Rental {self.pk}: {self.vehicle.vin} -> {self.customer.name}"

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def days_rented(self):
        """Calculate days rented - uses actual_return_date if available, otherwise expected_return_date."""
        from django.utils import timezone
        if self.actual_return_date:
            return (self.actual_return_date - self.rental_date).days
        # If no actual return date, calculate based on expected return date from rental start
        if self.expected_return_date and self.rental_date:
            # Ensure both datetimes are in the same timezone for comparison
            if timezone.is_aware(self.expected_return_date) and timezone.is_naive(self.rental_date):
                expected = timezone.make_naive(self.expected_return_date)
            elif timezone.is_naive(self.expected_return_date) and timezone.is_aware(self.rental_date):
                expected = timezone.make_aware(self.expected_return_date, timezone.get_current_timezone())
            elif timezone.is_aware(self.expected_return_date) and timezone.is_aware(self.rental_date):
                expected = self.expected_return_date
            else:
                expected = self.expected_return_date
            return (expected - self.rental_date).days
        return (timezone.now() - self.rental_date).days if self.rental_date else 0

    def calculate_charge(self):
        """Calculate rental charge without saving to database."""
        if not self.total_charge:
            from django.utils import timezone
            days = self.days_rented
            daily_rate = self.vehicle.daily_rate if self.vehicle else 0
            self.total_charge = days * daily_rate
        return self.total_charge

    def save(self, *args, **kwargs):
        """Override save to calculate charge and update vehicle status on creation."""
        is_create = self._state.adding
        
        # Update vehicle status only on creation (not on update)
        if is_create and self.vehicle:
            self.vehicle.status = 'rented'
            self.vehicle.save(update_fields=['status'])
        
        # Call super() first to ensure rental_date and other auto fields are set
        super().save(*args, **kwargs)
        
        # Calculate charge after save when rental_date is available (only on creation)
        if is_create and not self.total_charge and self.vehicle:
            days = self.days_rented
            daily_rate = self.vehicle.daily_rate
            self.total_charge = days * daily_rate
            # Save only the total_charge field
            super().save(update_fields=['total_charge'])