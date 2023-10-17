from rest_framework import permissions


class BaseDelegationPermission(permissions.BasePermission):
    """
    Default permission class. Developers should override the has_permission method.
    """
    def has_permission(self, request, view):
        return False


class CanCreateDelegationMixin:
    def has_create_permission(self, request, view):
        # default logic for creation, can be overridden
        return request.user.is_authenticated

class CanRevokeDelegationMixin:
    def has_revoke_permission(self, request, view, obj=None):
        # default logic for revocation, can be overridden
        return obj.delegator == request.user
