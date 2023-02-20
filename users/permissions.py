import re
from typing import List, Generator


class Permissions:
    _thumbnail_size_permission_codename_unformatted = 'can_get_thumbnail_{0}px'
    _thumbnail_size_permission_name_unformatted = 'Can get a link to a thumbnail with height of {0}px'

    ORIGINAL_IMAGE_PERMISSION_CODENAME = 'can_get_original_image'
    ORIGINAL_IMAGE_PERMISSION_NAME = 'Can get a link to the originally uploaded image'

    EXPIRING_IMAGE_PERMISSION_CODENAME = 'can_get_expiring_image'
    EXPIRING_IMAGE_PERMISSION_NAME = 'Can get an expiring link to the original image (300 to 30 000 seconds'

    # Stores pixel-size in .group(1)
    THUMBNAIL_PERMISSION_REGEX = re.compile(_thumbnail_size_permission_codename_unformatted.format(r'(\d+)'))

    @classmethod
    def iter_allowed_thumbnail_sizes(cls, user) -> Generator[int, None, None]:
        for permission in user.get_all_permissions():
            search = cls.THUMBNAIL_PERMISSION_REGEX.search(permission)
            if search:
                yield int(search.group(1))

    @classmethod
    def has_original_image_permission(cls, user) -> bool:
        return any([cls.ORIGINAL_IMAGE_PERMISSION_CODENAME in p for p in user.get_all_permissions()])

    @classmethod
    def has_expiring_image_permission(cls, user) -> bool:
        return any([cls.EXPIRING_IMAGE_PERMISSION_CODENAME in p for p in user.get_all_permissions()])

    @classmethod
    def get_thumbnail_size_permission_codename(cls, size: int) -> str:
        return cls._thumbnail_size_permission_codename_unformatted.format(size)

    @classmethod
    def get_thumbnail_size_permission_name(cls, size: int) -> str:
        return cls._thumbnail_size_permission_name_unformatted.format(size)

    # Returns True on successful creation, False if permission already exists
    @staticmethod
    def create_permission(codename: str, name: str) -> bool:
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
            return True
        return False

    # Returns True on successful deletion, False if permission does not exist
    @staticmethod
    def delete_permission(codename: str) -> bool:
        from django.contrib.auth.models import Permission

        permissions = Permission.objects.filter(codename=codename)
        if permissions:
            permissions.delete()
            return True
        return False

    # Returns True on successful creation, False if group already exists
    @staticmethod
    def create_group_with_permissions(name: str, permission_codenames: List[str]) -> bool:
        from django.contrib.auth.models import Permission, Group

        group, created = Group.objects.get_or_create(name=name)
        if created:
            for codename in permission_codenames:
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)
            return True
        return False
