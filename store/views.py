from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductListSerializer
from .filters import ProductFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    search_fields = ['name']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Return top 8 in-stock products ordered by newest."""
        products = self.get_queryset().filter(stock__gt=0)[:8]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
