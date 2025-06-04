from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer
from products.utils import get_first_serializer_error
from django.shortcuts import get_object_or_404


class AddressViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        address_serializer = AddressSerializer(addresses, many=True)
        return Response(address_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Addresss added successfully.'}, status=status.HTTP_201_CREATED)
        
        error = get_first_serializer_error(serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if not pk:
            return Response({'error': 'Address ID is required for update.'}, status=status.HTTP_400_BAD_REQUEST)

        address = get_object_or_404(Address, id=pk, user=request.user)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Address updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Address ID is required for deletion.'}, status=status.HTTP_400_BAD_REQUEST)

        address = get_object_or_404(Address, id=pk, user=request.user)
        address.delete()
        return Response({'message': 'Address deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
