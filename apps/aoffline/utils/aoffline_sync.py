from apps.account.models import Role, User, UserRoles
from apps.aoffline.models import (
    Role as Role_offline, User as User_offline, UserRoles as UserRoles_offline)


class AccountFullSynchronization:
    def __init__(self):
        pass

    def full_sync(self):
        self.full_role_sync()
        self.full_user_sync()
        self.user_roles_sync()

    def full_role_sync(self):
        Role_offline.objects.using('default').all().delete()
        roles = Role.objects.using('bloom').all()
        for role in roles:
            off_role = Role_offline.objects.using('default').create(
                id=role.id,
                defaults={
                    'name': role.name,
                    'description': role.description,
                }
            )
            off_role.save()

    def full_user_sync(self):
        User_offline.objects.using('default').all().delete()
        users = User.objects.using('bloom').all()
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

    def full_user_roles_sync(self):
        UserRoles_offline.objects.using('default').all().delete()
        user_roles = UserRoles.objects.using('bloom').all()
        for user_role in user_roles:
            UserRoles_offline.objects.using('default').update_or_create(
                id=user_role.id,
                user_id=user_role.user_id,
                role_id=user_role.role_id,
                update_at=user_role.update_at,
            )
