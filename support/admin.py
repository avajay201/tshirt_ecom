from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin):
    readonly_fields = ('submitted_at', )
