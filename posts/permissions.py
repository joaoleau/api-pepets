from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.api.permissions import *


class IsAuthorOrIsAuthenticatedReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.pet.owner == request.user and request.user.is_authenticated) or (
            request.user.is_authenticated and request.method in SAFE_METHODS
        )
