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




    def __str__(self):
        return self.title
