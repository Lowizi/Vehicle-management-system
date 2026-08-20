from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('vehicles', views.VehicleViewSet.as_view({'get': 'list', 'post': 'create'}), name='vehicle-list'),
    path('vehicles/<uuid:pk>', views.VehicleViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='vehicle-detail'),
]