from django.contrib.auth.models import User
from tests.data.temp_users import TempUsers
from users.permissions import Permissions


class TestPermissions:
    def test_user_iterate_allowed_thumbnail_sizes(self):
        TempUsers.populate_users()
        premium = User.objects.get(username=TempUsers.premium['username'])
        sizes = sorted([size for size in Permissions.iter_allowed_thumbnail_sizes(premium)])

        assert len(sizes) == 2, 'Thumbnail sizes are not parsed correctly'
        assert sizes[0] == 200 and sizes[1] == 400, 'Thumbnail sizes are not parsed correctly'

    def test_enterprise_rights(self):
        TempUsers.populate_users()
        enterprise = User.objects.get(username=TempUsers.enterprise['username'])
        assert Permissions.has_expiring_image_permission(enterprise) is True,\
            'Enterprise users should have permission to get expiring images, have not'
