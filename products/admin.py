from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Product, ProductVariant, ProductVariantImage, ProductReview
from unfold.admin import StackedInline, TabularInline


# @admin.register(Category)
# class CategoryAdmin(ModelAdmin):
#     pass

class ProductVariantImageInline(TabularInline):
    model = ProductVariantImage
    extra = 1

class ProductVariantInline(StackedInline):
    model = ProductVariant
    extra = 1
    show_change_link = True

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    readonly_fields = ('created_at', )
    inlines = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    inlines = [ProductVariantImageInline]

@admin.register(ProductVariantImage)
class ProductVariantImageItemAdmin(ModelAdmin):
    pass

@admin.register(ProductReview)
class ProductReviewItemAdmin(ModelAdmin):
    readonly_fields = ('created_at', )
