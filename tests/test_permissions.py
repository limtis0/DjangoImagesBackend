from django.contrib.auth.models import User
from tests.data.fixture_users import Users
from users.permissions import user_iterate_allowed_thumbnail_sizes


class TestPermissions:
    def test_user_iterate_allowed_thumbnail_sizes(self):
        Users.populate_users()
        premium = User.objects.get(username=Users.premium['username'])
        sizes = sorted([size for size in user_iterate_allowed_thumbnail_sizes(premium)])

        assert len(sizes) == 2, 'Thumbnail sizes are not parsed correctly'
        assert sizes[0] == 200 and sizes[1] == 400, 'Thumbnail sizes are not parsed correctly'
