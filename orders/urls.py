from django.urls import path
from .views import AddressAPIView


urlpatterns = [
    path('addresses/', AddressAPIView.as_view(), name='address'),
]
