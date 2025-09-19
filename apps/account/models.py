from django.db import models


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        app_label = "account"
        ordering = ['id']


class User(models.Model):
    username = models.CharField(db_index=True, max_length=30, unique=True)
    password = models.CharField(max_length=128)
    fio = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    departmant = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    room = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        app_label = "account"
        managed = False
        ordering = ['id']


class UserRoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "account"
        managed = False
        unique_together = ('user', 'role')
        ordering = ['id']
