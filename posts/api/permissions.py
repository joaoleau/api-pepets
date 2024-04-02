from rest_framework.permissions import BasePermission, SAFE_METHODS
from posts.models import Pet


class IsAuthorOrIsAuthenticatedReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user and request.user.is_authenticated) or (
            request.user.is_authenticated and request.method in SAFE_METHODS
        )


class IsAuthorObj(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user and request.user.is_authenticated


class IsAuthorView(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return (
            Pet.objects.filter(owner=request.user).exists()
            and request.user.is_authenticated
        )
