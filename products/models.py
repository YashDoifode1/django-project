from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    affiliate_link = models.URLField()
    image = models.ImageField(upload_to='products/', blank=True, null=True, default='products/default.jpeg')

    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    review_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    discount_percentage = models.PositiveIntegerField(blank=True, null=True)
    key_features = models.TextField(blank=True, null=True)  # comma-separated
    specifications = models.TextField(blank=True, null=True)  # comma-separated "Name: Value"
    @property
    def key_features_list(self):
        if self.key_features:
            return [kf.strip() for kf in self.key_features.split(',')]
        return []

    def __str__(self):
        return self.title

from django.contrib.auth.models import User
from django.db import models
from products.models import Product

class SavedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} saved {self.product.title}"

