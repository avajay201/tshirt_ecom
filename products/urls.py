from django.urls import path
from .views import ProductListAPIView, HomeProductListAPIView, ProductDetailAPIView, SubmitProductReview


urlpatterns = [
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('home-products/', HomeProductListAPIView.as_view(), name='product-list'),
    path('<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('submit-review/', SubmitProductReview.as_view(), name='submit-review'),
]
