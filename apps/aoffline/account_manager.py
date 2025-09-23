from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager

from .exceptions import EmptyUserException, PasswordEmptyException


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        '''Создание пользователя'''
        if not username:
            raise EmptyUserException

        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        '''Создание суперпользователя'''
        if not username:
            raise EmptyUserException
        if not password:
            raise PasswordEmptyException
        from apps.aoffline.models import Role, UserRoles

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('created_at', datetime.now())
        extra_fields.setdefault('updated_at', datetime.now())
        user = self.model(id=1, username=username, **extra_fields)
        user.set_password(password)
        user.save()

        role = Role.objects.filter(name='admin').first()
        if not role:
            role = Role.objects.create(id=1, name='admin')
        UserRoles.objects.update_or_create(user=user, role=role)
        return user

    def get_queryset(self):
        '''Получение списка всех аккаунтов'''
        return BaseUserManager.get_queryset(self)
