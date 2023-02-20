import pytest
from images.models import Image
from tests.data.temp_images import TempImages
from tests.data.temp_users import TempUsers
from hexOceanBackend.settings import DEBUG
from django.contrib.auth.models import User

URL = '/api/upload'


class TestUpload:
    @pytest.mark.xfail(condition=DEBUG, reason='Switching unauthorized users to users.TestUser if DEBUG is True')
    def test_unauthorized(self, api_client):
        response = api_client.post(URL, data=None)
        assert response.status_code == 401, f'{URL} should return 401 to unauthorized users'

    def test_upload_valid(self, api_client):
        TempUsers.populate_users()

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        image = TempImages.generate_image('.jpg', (100, 100))

        response = api_client.post(URL, {'title': 'title', 'image': image}, format='multipart')
        user = User.objects.get(username=TempUsers.basic['username'])

        assert response.status_code == 200, f'{URL} has not processed valid data correctly'
        assert Image.objects.filter(user=user).count() == 1, f'{URL} should create a new Image object'
        assert len(response.data['thumbnails']) == 1, f'{URL} should return thumbnails on response'

    def test_upload_invalid(self, api_client):
        TempUsers.populate_users()

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        image = TempImages.generate_image('.bmp', (100, 100))

        response = api_client.post(URL, {'title': 'title', 'image': image}, format='multipart')
        user = User.objects.get(username=TempUsers.basic['username'])

        assert response.status_code == 400, f'{URL} should reject invalid extensions'
        assert Image.objects.filter(user=user).count() == 0, f'{URL} should not save invalid images'
