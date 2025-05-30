from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Banner


@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    readonly_fields = ('created_at', )
