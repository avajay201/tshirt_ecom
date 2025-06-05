from django.urls import path
from .views import AddressAPIView, ShippingChargesAPIView


urlpatterns = [
    path('addresses/', AddressAPIView.as_view(), name='address'),
    path('shipping-charges/', ShippingChargesAPIView.as_view(), name='shipping_charges'),
]
