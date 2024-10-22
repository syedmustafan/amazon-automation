from rest_framework import serializers

from .models import Product, Brand


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'asin', 'sku', 'image', 'brand']


class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['name', 'products', 'product_count']

    def get_product_count(self, obj):
        return obj.products.count()
