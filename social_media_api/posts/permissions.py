from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read only safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # write allowed only to owner
        return obj.author == request.user
