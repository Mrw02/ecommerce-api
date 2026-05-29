from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from store.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_name', 'product_price', 'quantity', 'subtotal')

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs.get('quantity', 1)
        if quantity > product.stock:
            raise serializers.ValidationError(
                {'quantity': f'Only {product.stock} units available.'}
            )
        return attrs


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total', 'item_count', 'updated_at')


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'unit_price', 'quantity', 'subtotal')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'status', 'shipping_address', 'total_amount', 'items', 'created_at')
        read_only_fields = ('id', 'status', 'total_amount', 'created_at')


class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
