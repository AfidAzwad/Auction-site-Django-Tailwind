from .models import BID
from .serializers import BidSerializer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .permissions import BidIsCreatedByOrReadonly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



class BIDViewSet(ModelViewSet):
    lookup_field = 'bid_id'
    queryset = BID.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated, BidIsCreatedByOrReadonly]
    
    def get_queryset(self):
        user = self.request.user
        # Check if a query parameter, e.g., 'bid_by_only', is present in the request
        owner_only = self.request.query_params.get('bid_by_only', False)
        if owner_only:
            queryset = BID.objects.filter(auction_created_by=user)
        else:
            queryset = BID.objects.all()
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        user = request.user
        auction_id = request.data.get('auction_id')
        existing_bid = BID.objects.filter(bider_id=user, auction_id=auction_id).first()

        if existing_bid:
            serializer = self.get_serializer(existing_bid, data=request.data)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(bider_id=user)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not BidIsCreatedByOrReadonly().has_permission(request, self):
            return Response({"detail": "You do not have permission to update this object."}, status=status.HTTP_403_FORBIDDEN)
        
        if instance.auction_id.status in ["ended"]:
            return Response(
                {"detail": "You cannot update this bid because the auction is ended."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.auction_id.status in ["ended"]:
            return Response(
                {"detail": "You cannot delete this bid because the auction is ended."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)