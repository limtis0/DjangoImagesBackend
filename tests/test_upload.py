import pytest

from images.models import Image
from tests.data.temp_images import generate_image
from tests.data.fixture_users import Users
from hexOceanBackend.settings import DEBUG

URL = '/api/upload'


class TestUpload:
    @pytest.mark.xfail(condition=DEBUG, reason='Switching unauthorized users to users.TestUser if DEBUG is True')
    def test_unauthorized(self, api_client):
        response = api_client.post(URL, data=None)

        assert response.status_code == 401, f'{URL} is not giving 401 for unauthorized users'

    def test_upload_valid(self, api_client):
        Users.populate_users()

        api_client.login(username=Users.basic['username'], password=Users.basic['password'])
        image = generate_image('.jpg', (100, 100))

        count_before = Image.objects.count()
        response = api_client.post(URL, {'title': 'title', 'image': image}, format='multipart')

        assert response.status_code == 200, f'{URL} has not processed valid data correctly'
        assert Image.objects.count() - count_before == 1, f'{URL} is not creating a new Image object'
        assert len(response.data['thumbnails']) == 1, f'{URL} is not creating thumbnails on response'
