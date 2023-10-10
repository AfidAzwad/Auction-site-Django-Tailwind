from .models import AUCTION, BID
from .serializers import AuctionSerializer, BidSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .permissions import AuctionIsCreatedByOrReadonly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .services import AuctionService
from rest_framework import status



class AuctionViewSet(ModelViewSet):
    queryset = AUCTION.objects.all()
    serializer_class = AuctionSerializer
    permission_classes =[IsAuthenticated, AuctionIsCreatedByOrReadonly]
    
    def get_queryset(self):
        user = self.request.user
        # Check if a query parameter, e.g., 'created_by_only', is present in the request
        owner_only = self.request.query_params.get('created_by_only', False)
        if owner_only:
            queryset = AUCTION.objects.filter(auction_created_by=user)
        else:
            queryset = AUCTION.objects.all()
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['auction_created_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        AuctionService.find_auction_winner(request)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        AuctionService.find_auction_winner(request,instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not AuctionIsCreatedByOrReadonly().has_permission(request, self):
            return Response({"detail": "You do not have permission to update this object."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status in ["confirm", "ended"]:
            return Response(
                {"detail": "You cannot delete this auction because it is in the confirm or ended state."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
