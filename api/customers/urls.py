from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('customers', views.CustomerViewSet.as_view({'get': 'list', 'post': 'create'}), name='customer-list'),
    path('customers/<uuid:pk>', views.CustomerViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='customer-detail'),
]