from django.db import models
from accounts.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="product_categories/")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = self.name.lower().replace(" ", "_")
            slug = slugify(base_slug, allow_unicode=True)

            counter = 1
            unique_slug = slug
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}_{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    features = models.TextField(help_text="New line separated of product features")
    # category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.TextField(blank=True, help_text="Comma-separated tags")
    is_active = models.BooleanField(default=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    SIZE_CHOICES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Unisex', 'Unisex')]
    AGE_GROUP_CHOICES = [('Kids', 'Kids'), ('Teens', 'Teens'), ('Adults', 'Adults')]

    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color_name = models.CharField(max_length=50, help_text="Display name for the color (e.g., 'Red', 'Sky Blue').")
    color_code = models.CharField(max_length=7, help_text="Hex code for the color (e.g., '#FF0000').")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offer_percentage = models.PositiveIntegerField(null=True, blank=True, help_text="Auto-calculated if offer_price is given")


    def __str__(self):
        return f"{self.product.name} - {self.size}/{self.color_name}"

    def get_effective_price(self):
        if self.offer_price and self.offer_price < self.price:
            return self.offer_price
        return self.price

    def save(self, *args, **kwargs):
        if self.offer_price and self.offer_price < self.price:
            self.offer_percentage = int(round(((self.price - self.offer_price) / self.price) * 100))
        else:
            self.offer_percentage = None
        super().save(*args, **kwargs)

class ProductVariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_variants/")
    alt_text = models.CharField(max_length=255, default='Product Image')

    def __str__(self):
        return f"Image for {self.variant}"

class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.rating} star by {self.user.username if self.user else 'Anonymous'}"
