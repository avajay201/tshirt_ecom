from django.urls import path
from .views import RegisterAPIView, LoginAPIView, VerifyAccount


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify-account/<uidb64>/<token>/', VerifyAccount.as_view(), name='verify_account'),
]
