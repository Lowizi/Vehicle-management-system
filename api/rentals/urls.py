from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('rentals', views.RentalViewSet.as_view({'get': 'list', 'post': 'create'}), name='rental-list'),
]