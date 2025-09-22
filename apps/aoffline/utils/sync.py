from apps.account.models import Role, User, UserRoles
from apps.aoffline.models import (
    Role as Role_offline, User as User_offline, UserRoles as UserRoles_offline)


class AccountSynchronization:
    def __init__(self):
        pass

    def full_sync(self):
        self.role_sync()
        self.user_sync()
        self.user_roles_sync()

    def role_sync(self):
        off_roles = Role_offline.objects.using('default').all().order_by('update_at')
        if not off_roles:
            roles = Role.objects.using('bloom').all()
        else:
            roles = Role.objects.using('bloom').filter(update_at__gte=off_roles[0].update_at)
        for role in roles:
            Role_offline.objects.using('default').update_or_create(
                id=role.id,
                name=role.name,
                description=role.description,
                update_at=role.update_at,
            )

    def user_sync(self):
        off_users = User_offline.objects.using('default').all().order_by('updated_at')
        if not off_users:
            users = User.objects.using('bloom').all()
        else:
            users = User.objects.using('bloom').filter(updated_at__gte=off_users[0].updated_at)
        for user in users:
            User_offline.objects.using('default').update_or_create(
                id=user.id,
                fio=user.fio,
                username=user.username,
                password=user.password,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                departmant=user.departmant,
                position=user.position,
                room=user.room,
            )

    def user_roles_sync(self):
        off_user_roles = UserRoles_offline.objects.using('default').all().order_by('update_at')
        if not off_user_roles:
            user_roles = UserRoles.objects.using('bloom').all()
        else:
            user_roles = UserRoles.objects.using('bloom').filter(update_at__gte=off_user_roles[0].update_at)
        for user_role in user_roles:
            UserRoles_offline.objects.using('default').update_or_create(
                id=user_role.id,
                user_id=user_role.user_id,
                role_id=user_role.role_id,
                update_at=user_role.update_at,
            )
