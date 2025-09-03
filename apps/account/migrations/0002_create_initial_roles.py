from django.db import migrations


def create_roles(apps, _schema_editor):
    role = apps.get_model('account', 'Role')
    roles = [
        {"name": "admin", "description": "Full access to all features"},
        {"name": "arrival_reader", "description": "Can read arrival data"},
        {"name": "order_writer", "description": "Can write orders"},
        {"name": "container_writer", "description": "Can write containers"},
        {"name": "declaration_writer", "description": "Can write declarations"},
        {"name": "content_writer", "description": "Can write content"},
    ]
    for role_data in roles:
        if not role.objects.filter(name=role_data["name"]).exists():
            role.objects.create(**role_data)


def reverse_roles(apps, _schema_editor):
    role = apps.get_model('account', 'Role')
    role_names = [
        "admin", "arrival_reader", "order_writer",
        "container_writer", "declaration_writer", "content_writer"
    ]
    role.objects.filter(name__in=role_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_roles, reverse_roles),
    ]
