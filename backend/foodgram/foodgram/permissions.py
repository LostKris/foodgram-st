from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class IsAuthenticatedOrReadOnlyAndNotMe(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and view.action != 'me':
            return True
        return request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) is type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff