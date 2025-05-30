from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializer


class ProductPagination(PageNumberPagination):
    page_size = 12

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
