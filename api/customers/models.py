import uuid
from django.db import models


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Full Name', max_length=100)
    email = models.EmailField('Email Address', unique=True)
    phone = models.CharField('Phone Number', max_length=20, blank=True)
    license_number = models.CharField('Driver\'s License Number', max_length=50, unique=True)
    created_at = models.DateTimeField('Created At', auto_now_add=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['name']

    def __str__(self):
        return self.name