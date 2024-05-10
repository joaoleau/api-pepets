from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrIsAuthenticatedReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user and request.user.is_authenticated) or (
            request.user.is_authenticated and request.method in SAFE_METHODS
        )


class IsAuthorObject(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.pet.owner == request.user and request.user.is_authenticated
