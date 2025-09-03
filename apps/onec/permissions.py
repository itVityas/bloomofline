from Bloom.permission import RoleBasedPermission


class Warehouse1CPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'warehouse' and 'warehouse_writer'.
    - Other methods: Allowed only for 'admin' and 'warehouse_writer'.
    """
    allowed_roles_get = {'admin', 'warehouse', 'warehouse_writer'}
    allowed_roles_post = {'admin', 'warehouse_writer'}
    allowed_roles_update = {'admin', 'warehouse_writer'}
    allowed_roles_delete = {'admin', 'warehouse_writer'}
