from rest_framework import permissions


class IsSuperUserOrOwner(permissions.BasePermission):
    """
    A permission given when the user is a super user
    or when a user is the owner of the requested object
    """

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        return request.user == obj.owner


class IsOwner(permissions.BasePermission):
    """
    A permission given when a user is the owner of the requested object
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner