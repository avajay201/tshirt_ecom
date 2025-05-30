from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    readonly_fields = ('created_at', )

@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    pass
