from .serializers import CategorySerializer, ProductSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import CATEGORY, PRODUCT
from rest_framework.permissions import IsAuthenticated
from .permissions import ProductIsCreatedByOrReadonly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters



class CategoryViewSet(ModelViewSet):
    lookup_field = 'category_id'
    queryset = CATEGORY.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return super().get_permissions()

    
class ProductViewSet(ModelViewSet):
    lookup_field = 'product_id'
    queryset = PRODUCT.objects.all()
    permission_classes = [IsAuthenticated, ProductIsCreatedByOrReadonly]
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Enable search and ordering
    search_fields = ['product_name', 'product_owner__first_name']  # Fields to search
    ordering_fields = ['created_at']  # Fields for ordering
    
    pagination_class = PageNumberPagination
    page_size = 5
    
    def get_queryset(self):
        user = self.request.user
        # Check if a query parameter, e.g., 'owner_only', is present in the request
        owner_only = self.request.query_params.get('owner_only', False)

        if owner_only:
            queryset = PRODUCT.objects.filter(product_owner=user)
        else:
            queryset = PRODUCT.objects.all()
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['product_owner'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not ProductIsCreatedByOrReadonly().has_permission(request, self):
            return Response({"detail": "You do not have permission to update this object."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    