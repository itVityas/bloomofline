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
            roles_del = Role_offline.objects.using('default').all().exclude(
                id__in=[i['id'] for i in Role.objects.using('bloom').all().values('id')])
            roles_del.delete()
            roles = Role.objects.using('bloom').filter(update_at__gt=off_roles[0].update_at)
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
            users_del = User_offline.objects.using('default').all().exclude(
                id__in=[i['id'] for i in User.objects.using('bloom').all().values('id')])
            users_del.delete()
            users = User.objects.using('bloom').filter(updated_at__gt=off_users[0].updated_at)
        for user in users:
            defaults = {
                'fio': user.fio,
                'username': user.username,
                'password': user.password,
                'is_active': user.is_active,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'departmant': user.departmant,
                'position': user.position,
                'room': user.room,
            }
            User_offline.objects.using('default').update_or_create(
                id=user.id,
                defaults=defaults
            )

    def user_roles_sync(self):
        off_user_roles = UserRoles_offline.objects.using('default').all().order_by('update_at')
        if not off_user_roles:
            user_roles = UserRoles.objects.using('bloom').all()
        else:
            user_roles_del = UserRoles_offline.objects.using('default').all().exclude(
                id__in=[i['id'] for i in UserRoles.objects.using('bloom').all().values('id')])
            user_roles_del.delete()
            user_roles = UserRoles.objects.using('bloom').filter(update_at__gt=off_user_roles[0].update_at)
        for user_role in user_roles:
            UserRoles_offline.objects.using('default').update_or_create(
                id=user_role.id,
                user_id=user_role.user_id,
                role_id=user_role.role_id,
                update_at=user_role.update_at,
            )
