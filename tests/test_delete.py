import pytest
import shortuuid
from django.contrib.auth.models import User
from images.models import Image
from hexOceanBackend.settings import DEBUG
from tests.data.temp_users import TempUsers
from tests.data.temp_images import TempImages
from django.urls import reverse
from api.views import delete_image


URL = '/api/delete/'


class TestDelete:
    @pytest.mark.xfail(condition=DEBUG, reason='Switching unauthorized users to users.TestUser if DEBUG is True')
    def test_unauthorized(self, api_client):
        response = api_client.delete(reverse(delete_image, args=['randomString']), data=None)
        assert response.status_code == 401, f'{URL} should return 401 to unauthorized users'

    def test_delete_valid(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        user = User.objects.get(username=TempUsers.basic['username'])
        image = Image.objects.filter(user=user).first()

        file_path = image.get_original_file_path()

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        response = api_client.delete(reverse(delete_image, args=[image.uuid]), None)

        assert response.status_code == 200, f'{URL} should delete an Image from DB on valid request'
        assert not file_path.exists(), f'{URL} should delete the Image files on valid request'

    def test_delete_invalid_user(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        premium_user = User.objects.get(username=TempUsers.premium['username'])
        image = Image.objects.filter(user=premium_user).first()

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        response = api_client.delete(reverse(delete_image, args=[image.uuid]), None)

        assert response.status_code == 404, f'{URL} should return 404 on invalid user'

    def test_delete_invalid_image(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        response = api_client.delete(reverse(delete_image, args=[shortuuid.uuid()]), None)

        assert response.status_code == 404, f'{URL} should return 404 on non-existent image'
