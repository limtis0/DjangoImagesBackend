from typing import List


def create_permission(codename: str, name: str):
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from users.models import Profile

    content_type = ContentType.objects.get_for_model(Profile)
    if not Permission.objects.filter(content_type=content_type, codename=codename):
        Permission.objects.create(
            codename=codename,
            name=name,
            content_type=content_type,
        )


def remove_permission(codename: str, name: str):
    from django.contrib.auth.models import Permission

    Permission.objects.filter(codename=codename, name=name).delete()


def create_group_with_permissions(name: str, permission_codenames: List[str]):
    from django.contrib.auth.models import Permission, Group

    group, created = Group.objects.get_or_create(name=name)
    if created:
        for codename in permission_codenames:
            permission = Permission.objects.get(codename=codename)
            group.permissions.add(permission)
