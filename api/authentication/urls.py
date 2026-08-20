from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login', views.login, name='login'),
    path('verify', views.verify_token, name='verify-token'),
]