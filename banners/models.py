from django.db import models


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Smaller values show first.")
    created_at = models.DateTimeField(auto_now_add=True)
