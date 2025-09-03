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
        from apps.account.models import Role, UserRoles

        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()

        role = Role.objects.filter(name='admin').first()
        if not role:
            role = Role.objects.create(name='admin')
        UserRoles.objects.create(user=user, role=role)
        return user

    def get_queryset(self):
        '''Получение списка всех аккаунтов'''
        return BaseUserManager.get_queryset(self)
