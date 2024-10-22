from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    amazon_url = models.URLField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    asin = models.CharField(max_length=20, unique=True)
    sku = models.CharField(max_length=50, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
