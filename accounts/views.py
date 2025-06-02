from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from products.utils import get_first_serializer_error
from .utils import verify_account


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            created_data = serializer.save()
            return Response(created_data, status=status.HTTP_201_CREATED)
        error = get_first_serializer_error(serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        error = get_first_serializer_error(serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

class VerifyAccount(APIView):
    def get(self, request, uidb64, token):
        is_verified = verify_account(uidb64, token)
        return render(request, 'email/account_verified.html', {'status': is_verified})
