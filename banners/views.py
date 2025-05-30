from rest_framework import generics
from .models import Banner
from .serializers import BannerSerializer


class BannerListAPIView(generics.ListAPIView):
    queryset = Banner.objects.filter(is_active=True).order_by('display_order')
    serializer_class = BannerSerializer
