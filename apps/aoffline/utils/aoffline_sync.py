import time

from django.db import transaction
import logging

from apps.account.models import Role, User, UserRoles
from apps.aoffline.models import (
    OfflineRole as Role_offline, OfflineUser as User_offline, OfflineUserRoles as UserRoles_offline)

logger = logging.getLogger(__name__)


class AccountFullSynchronization:
    def __init__(self, batch_size=1000):
        self.batch_size = batch_size

    def full_sync(self) -> dict:
        """
        Full synchronization of account app
        """
        try:
            with transaction.atomic():
                time_dict = {}
                time_roles = self.full_role_sync()
                time_users = self.full_user_sync()
                time_m2m = self.full_user_roles_sync()
                time_dict['roles'] = time_roles
                time_dict['users'] = time_users
                time_dict['m2m'] = time_m2m
                time_dict['full'] = time_roles + time_users + time_m2m
                return time_dict
        except Exception as e:
            raise e

    def full_role_sync(self) -> float:
        try:
            start_time = time.time()
            Role_offline.objects.all().delete()
            roles = Role.objects.all().values('id', 'name', 'description', 'create_at', 'update_at')
            for role in roles:
                off_role = Role_offline.objects.create(
                    id=role['id'],
                    name=role['name'],
                    description=role['description'],
                    create_at=role['create_at'],
                    update_at=role['update_at'],
                )
                off_role.save()
            stop_time = time.time()
            return stop_time - start_time
        except Exception as e:
            logger.error('full_role_sync' + str(e))
            raise e

    def full_user_sync(self) -> float:
        try:
            start_time = time.time()
            User_offline.objects.all().delete()
            users = User.objects.all().values('id', 'username', 'password', 'fio', 'is_active',
                                              'created_at', 'updated_at', 'departmant', 'position', 'room')
            for user in users:
                User_offline.objects.update_or_create(
                    id=user['id'],
                    fio=user['fio'],
                    username=user['username'],
                    password=user['password'],
                    is_active=user['is_active'],
                    created_at=user['created_at'],
                    updated_at=user['updated_at'],
                    departmant=user['departmant'],
                    position=user['position'],
                    room=user['room'],
                )
            stop_time = time.time()
            return stop_time - start_time
        except Exception as e:
            logger.error('full_user_sync' + str(e))
            raise e

    def full_user_roles_sync(self) -> float:
        try:
            start_time = time.time()
            UserRoles_offline.objects.all().delete()
            user_roles = UserRoles.objects.select_related('user', 'role').all().values(
                'id', 'user_id', 'role_id', 'create_at', 'update_at')
            for user_role in user_roles.iterator(chunk_size=self.batch_size):
                UserRoles_offline.objects.update_or_create(
                    id=user_role['id'],
                    user_id=user_role['user_id'],
                    role_id=user_role['role_id'],
                    update_at=user_role['update_at'],
                    create_at=user_role['create_at'],
                )
            stop_time = time.time()
            return stop_time - start_time
        except Exception as e:
            logger.error('full_user_roles_sync' + str(e))
            raise e
