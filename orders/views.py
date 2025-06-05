from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer
from products.utils import get_first_serializer_error
from django.shortcuts import get_object_or_404
from .utils import get_shipping_charges


class AddressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        address_serializer = AddressSerializer(addresses, many=True)
        return Response(address_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Addresss added successfully.', 'address': serializer.data}, status=status.HTTP_201_CREATED)
        
        error = get_first_serializer_error(serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        pk = request.data.pop('id')
        address = get_object_or_404(Address, id=pk, user=request.user)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Address updated successfully.', 'address': serializer.data}, status=status.HTTP_200_OK)
        error = get_first_serializer_error(serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Address ID is required for deletion.'}, status=status.HTTP_400_BAD_REQUEST)

        address = get_object_or_404(Address, id=pk, user=request.user)
        address.delete()
        return Response({'message': 'Address deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class ShippingChargesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            products = int(request.query_params.get('p'))
            print(request.query_params)
            delivery_postcode = request.query_params.get('d_pc')
            weight = products * 0.3
            shipping_charges = get_shipping_charges(delivery_postcode, weight)
            return Response(shipping_charges, status=status.HTTP_200_OK)
        except Exception as e:
            print('Shipping charges Error:', e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
