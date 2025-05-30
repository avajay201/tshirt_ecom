from django.db import models
from accounts.models import User
from django.utils import timezone


# class Coupon(models.Model):
#     DISCOUNT_TYPE_CHOICES = (
#         ('percent', 'Percentage'),
#         ('fixed', 'Fixed Amount'),
#     )

#     code = models.CharField(max_length=20, unique=True)
#     description = models.CharField(max_length=255, blank=True)
#     discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
#     discount_value = models.DecimalField(max_digits=10, decimal_places=2)
#     min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     active = models.BooleanField(default=True)
#     total_usage_limit = models.IntegerField(null=True, blank=True)
#     per_user_usage_limit = models.IntegerField(null=True, blank=True)

#     def is_valid(self):
#         now = timezone.now()
#         return self.active and self.valid_from <= now <= self.valid_to

#     def __str__(self):
#         return self.code

# class CouponUsage(models.Model):
#     coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     used_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('coupon', 'user')