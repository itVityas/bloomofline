from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .account_manager import AccountManager


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        using_db = 'default'
        managed = False
        ordering = ['id']


class User(AbstractBaseUser):
    username = models.CharField(db_index=True, max_length=30, unique=True)
    fio = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    departmant = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    room = models.CharField(max_length=30, blank=True, null=True)

    USERNAME_FIELD = 'username'

    objects = AccountManager()

    def __str__(self):
        return self.username

    class Meta:
        using_db = 'default'
        managed = False
        ordering = ['id']


class UserRoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        using_db = 'default'
        managed = False
        unique_together = ('user', 'role')
        ordering = ['id']
