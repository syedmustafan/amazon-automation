from django.contrib import admin
from .models import Brand, Product


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'amazon_url']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'asin', 'sku', 'brand']
    search_fields = ['name', 'asin', 'sku']
    list_filter = ['brand']
