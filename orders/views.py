from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Address, Order, OrderItem
from .serializers import AddressSerializer, OrderSerializer
from products.utils import get_first_serializer_error
from django.shortcuts import get_object_or_404
from .utils import get_shipping_charges
from products.models import ProductVariant
import json
from decimal import Decimal


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
            delivery_postcode = request.query_params.get('d_pc')
            weight = products * 0.3
            shipping_charges = get_shipping_charges(delivery_postcode, weight)
            return Response(shipping_charges, status=status.HTTP_200_OK)
        except Exception as e:
            print('Shipping charges Error:', e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            item_ids = request.data.get("items", [])
            address_id = request.data.get("shipping_address_id")
            address = get_object_or_404(Address, id=address_id, user=user)
            variants = ProductVariant.objects.filter(id__in=item_ids)
            if len(variants) != len(item_ids):
                return Response({"error": "One or more variants not found."}, status=status.HTTP_400_BAD_REQUEST)

            total_price = 0
            order_items = []
            weight = 0

            cart = request.user.cart

            for variant in variants:
                cart_item = cart.items.filter(variant__id=variant.id).first()
                if not cart_item:
                    return Response({'error': 'Something went wrong.'}, status=status.HTTP_400_BAD_REQUEST)
                
                price = variant.offer_price
                total_price += price * cart_item.quantity
                weight += 0.3 * cart_item.quantity
                order_items.append({"name": variant.product.name, "size": variant.size, "color": variant.color_name, "quantity": cart_item.quantity, "price": price, "image": variant.images.first().image})

            shipping_address = AddressSerializer(address).data
            shipping_charges = get_shipping_charges(shipping_address['postal_code'], weight)
            order = Order.objects.create(
                user=user,
                total_price=total_price + Decimal(shipping_charges['charges']),
                shipping_address=json.dumps(shipping_address),
                shipping_charges=shipping_charges['charges']
            )

            for item in order_items:
                OrderItem.objects.create(order=order, **item)

            for cart_item in cart.items.all():
                cart_item.delete()

            return Response({'message': 'Order placed successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('Order creation error:', e)
            return Response({'error': 'Something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        order_serializer = OrderSerializer(orders, many=True)
        return Response(order_serializer.data, status=status.HTTP_200_OK)
