from rest_framework import permissions


class ProductIsCreatedByOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of a product
        return obj.product_owner == request.user