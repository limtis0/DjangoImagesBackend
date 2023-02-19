from django.apps import AppConfig
from users.permissions import Permissions
from django.db.models.signals import post_migrate

PLAN_BASIC = 'Basic'
PLAN_PREMIUM = 'Premium'
PLAN_ENTERPRISE = 'Enterprise'


def create_basic_permissions(sender, **kwargs):
    Permissions.create_permission(
        Permissions.get_thumbnail_size_permission_codename(200),
        Permissions.get_thumbnail_size_permission_name(200),
    )

    Permissions.create_permission(
        Permissions.get_thumbnail_size_permission_codename(400),
        Permissions.get_thumbnail_size_permission_name(400),
    )

    Permissions.create_permission(
        Permissions.ORIGINAL_IMAGE_PERMISSION_CODENAME,
        Permissions.ORIGINAL_IMAGE_PERMISSION_NAME,
    )

    Permissions.create_permission(
        Permissions.EXPIRING_IMAGE_PERMISSION_CODENAME,
        Permissions.EXPIRING_IMAGE_PERMISSION_NAME,
    )


def create_basic_plans(sender, **kwargs):
    Permissions.create_group_with_permissions(PLAN_BASIC, [Permissions.get_thumbnail_size_permission_codename(200)])

    Permissions.create_group_with_permissions(PLAN_PREMIUM, [
        Permissions.get_thumbnail_size_permission_codename(200),
        Permissions.get_thumbnail_size_permission_codename(400),
        Permissions.ORIGINAL_IMAGE_PERMISSION_CODENAME,
    ])

    Permissions.create_group_with_permissions(PLAN_ENTERPRISE, [
        Permissions.get_thumbnail_size_permission_codename(200),
        Permissions.get_thumbnail_size_permission_codename(400),
        Permissions.ORIGINAL_IMAGE_PERMISSION_CODENAME,
        Permissions.EXPIRING_IMAGE_PERMISSION_CODENAME,
    ])


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        post_migrate.connect(create_basic_permissions, sender=self)
        post_migrate.connect(create_basic_plans, sender=self)
