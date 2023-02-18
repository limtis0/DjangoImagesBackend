from django.apps import AppConfig
from users.permissions import create_permission, create_group_with_permissions
from django.db.models.signals import post_migrate

PLAN_BASIC = 'Basic'
PLAN_PREMIUM = 'Premium'
PLAN_ENTERPRISE = 'Enterprise'

PERMISSION_THUMBNAIL_200 = 'can_get_thumbnail_200px'
PERMISSION_THUMBNAIL_400 = 'can_get_thumbnail_400px'
PERMISSION_ORIGINAL_IMAGE = 'can_get_original_image'
PERMISSION_EXPIRING_IMAGE = 'can_get_expiring_image'


def create_basic_permissions(sender, **kwargs):
    create_permission(PERMISSION_THUMBNAIL_200, 'Can get a link to a thumbnail with height of 200px')
    create_permission(PERMISSION_THUMBNAIL_400, 'Can get a link to a thumbnail with height of 400px')
    create_permission(PERMISSION_ORIGINAL_IMAGE, 'Can get a link to the originally uploaded image')
    create_permission(PERMISSION_EXPIRING_IMAGE, 'Can get an expiring link to the original image (300 to 30 000 seconds')


def create_basic_plans(sender, **kwargs):
    create_group_with_permissions(PLAN_BASIC, [PERMISSION_THUMBNAIL_200])

    create_group_with_permissions(PLAN_PREMIUM, [
        PERMISSION_THUMBNAIL_200, PERMISSION_THUMBNAIL_400, PERMISSION_ORIGINAL_IMAGE
    ])

    create_group_with_permissions(PLAN_ENTERPRISE, [
        PERMISSION_THUMBNAIL_200, PERMISSION_THUMBNAIL_400, PERMISSION_ORIGINAL_IMAGE, PERMISSION_EXPIRING_IMAGE
    ])


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        post_migrate.connect(create_basic_permissions, sender=self)
        post_migrate.connect(create_basic_plans, sender=self)
