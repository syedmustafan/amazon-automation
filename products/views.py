from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Brand, Product
from .serializers import BrandSerializer, ProductSerializer


class BrandProductListView(APIView):
    """
    API view to retrieve a brand and its associated products by brand ID.
    """

    def get(self, request, brand_id, *args, **kwargs):
        brand = get_object_or_404(Brand, id=brand_id)
        serializer = BrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductSearchView(ListAPIView):
    """
    API view to search for products by name.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned products to a given name,
        by filtering against a `name` query parameter in the URL.
        """
        query_param = self.request.query_params.get('name', None)
        if query_param:
            return Product.objects.filter(Q(name__icontains=query_param))
        return Product.objects.all()
