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
