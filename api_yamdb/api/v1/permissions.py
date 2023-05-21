from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff


class IsAdminOrUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAdminOrAuthorOrModerator(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)
