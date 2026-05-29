from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'description', 'price',
            'stock', 'in_stock', 'image', 'is_active',
            'category', 'category_name', 'created_at',
        )
        read_only_fields = ('id', 'slug', 'created_at')


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'price', 'in_stock', 'image', 'category_name')
