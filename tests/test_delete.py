import pytest
import shortuuid
from django.contrib.auth.models import User
from images.models import Image
from hexOceanBackend.settings import DEBUG
from tests.data.temp_users import TempUsers
from tests.data.temp_images import TempImages

URL = '/api/delete'


class TestDelete:
    @pytest.mark.xfail(condition=DEBUG, reason='Switching unauthorized users to users.TestUser if DEBUG is True')
    def test_unauthorized(self, api_client):
        response = api_client.post(URL, data=None)

        assert response.status_code == 401, f'{URL} is not giving 401 for unauthorized users'

    def test_delete_valid(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        user = User.objects.get(username=TempUsers.basic['username'])
        image = Image.objects.filter(user=user).first()

        file_path = image.get_file_path()

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        response = api_client.delete(f'{URL}/{image.uuid}', None)

        assert response.status_code == 200, f'{URL} has not deleted an image on valid request'
        assert not file_path.exists(), f'{URL} is not deleting the files on valid request'

    def test_delete_invalid_user(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        premium_user = User.objects.get(username=TempUsers.premium['username'])
        image = Image.objects.filter(user=premium_user).first()

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        response = api_client.delete(f'{URL}/{image.uuid}', None)

        assert response.status_code == 403, f'{URL} is not returning 403 on invalid user'

    def test_delete_invalid_image(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        response = api_client.delete(f'{URL}/{shortuuid.uuid()}', None)

        assert response.status_code == 404, f'{URL} is not returning 404 on non-existent image'
