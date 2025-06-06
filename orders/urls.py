from django.urls import path
from .views import AddressAPIView, ShippingChargesAPIView, OrderAPIView


urlpatterns = [
    path('addresses/', AddressAPIView.as_view(), name='address'),
    path('shipping-charges/', ShippingChargesAPIView.as_view(), name='shipping_charges'),
    path('', OrderAPIView.as_view(), name='create-order'),
]
