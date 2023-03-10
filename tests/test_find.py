import pytest
from hexOceanBackend.settings import DEBUG
from tests.data.temp_users import TempUsers
from tests.data.temp_images import TempImages
from django.contrib.auth.models import User
from images.models import Image
from django.urls import reverse
from api.views import find_images

URL = '/api/find/'


class TestFind:
    @pytest.mark.xfail(condition=DEBUG, reason='Switching unauthorized users to users.TestUser if DEBUG is True')
    def test_unauthorized(self, api_client):
        response = api_client.get(reverse(find_images, args=['Anything']))
        assert response.status_code == 401, f'{URL} should return 401 to unauthorized users'

    def test_find_one(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        user = User.objects.get(username=TempUsers.basic['username'])
        image = Image.objects.filter(user=user).first()

        response = api_client.get(reverse(find_images, args=[image.title]))
        assert response.status_code == 200, f'{URL} should return 200 for a valid search query'
        assert len(response.data) == 1, f'{URL} should have returned one image'

    def test_find_empty(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])

        response = api_client.get(reverse(find_images, args=['randomString']))
        assert response.status_code == 200, f'{URL} should return 200 to an empty search query'
        assert len(response.data) == 0, f'{URL} should return 0 objects, returns {len(response.data)}'

    def test_find_wildcard(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])

        response_star = api_client.get(reverse(find_images, args=['*']))
        response_percent = api_client.get(reverse(find_images, args=['%']))

        assert len(response_star.data) == 0, f'{URL} query should not have wildcard symbols'
        assert len(response_percent.data) == 0, f'{URL} query should not have wildcard symbols'
