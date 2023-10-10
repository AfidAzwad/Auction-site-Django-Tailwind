from rest_framework import permissions
 

class AuctionIsCreatedByOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of an auction
        return obj.auction_created_by == request.user
    
class BidIsCreatedByOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of an auction
        return obj.bider_id == request.user
    