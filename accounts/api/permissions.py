from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or (request.user and request.user.is_staff)


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwnerOrAdminOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user or (request.user and request.user.is_staff)
