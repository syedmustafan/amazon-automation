from django.urls import path

from .views import BrandProductListView, ProductSearchView

urlpatterns = [
    path('brands/<int:brand_id>/products/', BrandProductListView.as_view(), name='brand-products'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),

]
