from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .account_manager import AccountManager


# Create your models here.
class Role(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = "aoffline"
        ordering = ['id']


class User(AbstractBaseUser):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(db_index=True, max_length=30, unique=True)
    password = models.CharField(max_length=128)
    fio = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    departmant = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    room = models.CharField(max_length=30, blank=True, null=True)

    USERNAME_FIELD = 'username'

    objects = AccountManager()

    def __str__(self):
        return self.username

    class Meta:
        app_label = "aoffline"
        ordering = ['id']


class UserRoles(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField()

    class Meta:
        app_label = "aoffline"
        unique_together = ('user', 'role')
        ordering = ['id']
