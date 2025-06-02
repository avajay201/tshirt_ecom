from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartItemSerializer
from products.models import ProductVariant


class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        variant_id = request.data.get('variant_id')
        quantity = request.data.get('quantity', 1)

        variant = get_object_or_404(ProductVariant, id=variant_id)
        
        cart, created = Cart.objects.get_or_create(user=user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        user = request.user
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')

        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=user)

        if quantity is not None and quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            return Response({"detail": "Cart item quantity updated."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid quantity."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        item_id = request.data.get('item_id', None)

        cart = get_object_or_404(Cart, user=user)

        if item_id:
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            cart_item.delete()
            return Response({'detail': 'Item removed from cart.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            CartItem.objects.filter(cart=cart).delete()
            return Response({'detail': 'All items removed from cart.'}, status=status.HTTP_204_NO_CONTENT)
