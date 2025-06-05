from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Address, Order, OrderItem, FreeShippingPinCode


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    readonly_fields = ('created_at', )

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    readonly_fields = ('created_at', )

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    pass

@admin.register(FreeShippingPinCode)
class FreeShippingPinCodeAdmin(ModelAdmin):
    pass
