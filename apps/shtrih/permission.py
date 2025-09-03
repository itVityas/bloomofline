from Bloom.permission import RoleBasedPermission


class StrihPermission(RoleBasedPermission):
    """
    Permission for Strih operations.
    - GET: Allowed for all.
    - Other methods: Allowed only for 'admin' and 'strih'.
    """
    allowed_roles_get = None
    allowed_roles_post = {'admin', 'strih'}
    allowed_roles_update = {'admin', 'strih'}
    allowed_roles_delete = {'admin', 'strih'}
