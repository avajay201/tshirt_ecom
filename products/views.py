from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductsSerializer, ProductReviewsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .utils import get_first_serializer_error
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend


class ProductPagination(PageNumberPagination):
    page_size = 12

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).all()
    serializer_class = ProductsSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

class HomeProductListAPIView(APIView):
    def get(self, request):
        featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:12]
        featured_products_serializer = ProductsSerializer(featured_products, many=True)
        return Response({'featured_products': featured_products_serializer.data, 'recommended_products': featured_products_serializer.data})

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductsSerializer
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class SubmitProductReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user
        serializer = ProductReviewsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Review submitted successfully", "review": serializer.data}, status=status.HTTP_201_CREATED)
        error = get_first_serializer_error(serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
