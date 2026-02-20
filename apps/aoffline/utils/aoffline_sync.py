from apps.account.models import Role, User, UserRoles
from apps.aoffline.models import (
    OfflineRole as Role_offline, OfflineUser as User_offline, OfflineUserRoles as UserRoles_offline)


class AccountFullSynchronization:
    def __init__(self):
        pass

    def full_sync(self):
        self.full_role_sync()
        self.full_user_sync()
        self.full_user_roles_sync()

    def full_role_sync(self):
        Role_offline.objects.all().delete()
        roles = Role.objects.all()
        for role in roles:
            off_role = Role_offline.objects.create(
                id=role.id,
                name=role.name,
                description=role.description,
                create_at=role.create_at,
                update_at=role.update_at,
            )
            off_role.save()

    def full_user_sync(self):
        User_offline.objects.all().delete()
        users = User.objects.all()
        for user in users:
            User_offline.objects.update_or_create(
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

    def full_user_roles_sync(self):
        UserRoles_offline.objects.all().delete()
        user_roles = UserRoles.objects.all()
        for user_role in user_roles:
            UserRoles_offline.objects.update_or_create(
                id=user_role.id,
                user_id=user_role.user_id,
                role_id=user_role.role_id,
                update_at=user_role.update_at,
                create_at=user_role.create_at,
            )
