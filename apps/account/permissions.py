from rest_framework.permissions import BasePermission


class AccountPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        user_roles = list([userroles.role.name for userroles in request.user.userroles_set.all()])
        if 'admin' in user_roles:
            return True
        return False
