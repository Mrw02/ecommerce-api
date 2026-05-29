from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer, CartItemSerializer,
    OrderSerializer, CheckoutSerializer,
)


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        cart, _ = Cart.objects.prefetch_related('items__product').get_or_create(user=self.request.user)
        return cart


class CartItemAddView(APIView):
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
            if item.quantity > product.stock:
                return Response(
                    {'quantity': f'Only {product.stock} units available.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item.save()

        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemUpdateView(generics.UpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_destroy(self, instance):
        instance.delete()


class CheckoutView(APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.select_related('product').all()

        if not items.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate stock for all items before creating order
        for item in items:
            if item.quantity > item.product.stock:
                return Response(
                    {'detail': f'"{item.product.name}" has only {item.product.stock} units left.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        total = sum(item.subtotal for item in items)
        order = Order.objects.create(
            user=request.user,
            shipping_address=serializer.validated_data['shipping_address'],
            total_amount=total,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                unit_price=item.product.price,
                quantity=item.quantity,
            )
            # Deduct stock
            item.product.stock -= item.quantity
            item.product.save()

        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')
