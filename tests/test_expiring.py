import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from images.models import Image
from hexOceanBackend.settings import DEBUG
from tests.data.temp_users import TempUsers
from tests.data.temp_images import TempImages

URL = '/api/expiring/{0}/{1}'


class TestExpiring:
    @pytest.mark.xfail(condition=DEBUG, reason='Switching unauthorized users to users.TestUser if DEBUG is True')
    def test_unauthorized(self, api_client):
        response = api_client.post(URL, data=None)
        assert response.status_code == 401, f'{URL} should give 401 for unauthorized users'

    def test_create_valid(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        enterprise = User.objects.get(username=TempUsers.enterprise['username'])
        image = Image.objects.filter(user=enterprise).first()
        duration = 500

        api_client.login(username=TempUsers.enterprise['username'], password=TempUsers.enterprise['password'])
        response = api_client.get(URL.format(image.uuid, duration))

        assert response.status_code == 200, f'{URL} should return status code 200 on valid request'
        assert response.data['title'] == image.title, f'{URL} response data should contain "title" of the original Image'
        assert response.data['duration'] == duration, f'{URL} response data should contain correct duration'

        valid_until = response.data['valid_until']
        approx_valid_until = timezone.now() + timezone.timedelta(seconds=duration)
        epsilon = timezone.timedelta(seconds=10)

        assert abs(valid_until - approx_valid_until) < epsilon, \
            f'{URL} response data should contain correct "valid_until" field'

        assert response.data.get('url') is not None, f'{URL} response data should contain "url"'

    def test_update(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        enterprise = User.objects.get(username=TempUsers.enterprise['username'])
        image = Image.objects.filter(user=enterprise).first()

        old_duration = 500
        new_duration = 1000

        api_client.login(username=TempUsers.enterprise['username'], password=TempUsers.enterprise['password'])
        old_response = api_client.get(URL.format(image.uuid, old_duration))
        new_response = api_client.get(URL.format(image.uuid, new_duration))

        assert old_response.data['duration'] == old_duration and new_response.data['duration'] == new_duration, \
            f'{URL} should change "duration" to desired on update'

        assert old_response.data['url'] != new_response.data['url'], f'{URL} should change "url" on update'

        valid_until = new_response.data['valid_until']
        approx_valid_until = timezone.now() + timezone.timedelta(seconds=new_duration)
        epsilon = timezone.timedelta(seconds=10)
        assert abs(valid_until - approx_valid_until) < epsilon, \
            f'{URL} response data on update should contain correct "valid_until" field'

    def test_no_image(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        duration = 500

        api_client.login(username=TempUsers.enterprise['username'], password=TempUsers.enterprise['password'])
        response = api_client.get(URL.format('INVALID_UUID', duration))

        assert response.status_code == 404, f'{URL} should give 404 if image UUID is invalid'

    def test_duration_clamp(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        MIN_DURATION = 300
        MAX_DURATION = 30_000

        enterprise = User.objects.get(username=TempUsers.enterprise['username'])
        image = Image.objects.filter(user=enterprise).first()

        small_duration = 1
        api_client.login(username=TempUsers.enterprise['username'], password=TempUsers.enterprise['password'])
        small_duration_response = api_client.get(URL.format(image.uuid, small_duration))

        assert small_duration_response.status_code == 200, f'{URL} should give 200 even with duration < MIN'
        assert small_duration_response.data['duration'] == MIN_DURATION, f'{URL} should clamp duration'

        big_duration = 999_999
        big_duration_response = api_client.get(URL.format(image.uuid, big_duration))

        assert big_duration_response.status_code == 200, f'{URL} should give 200 even with duration > MAX'
        assert big_duration_response.data['duration'] == MAX_DURATION, f'{URL} should clamp duration'

    def test_no_access(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        basic = User.objects.get(username=TempUsers.basic['username'])
        image = Image.objects.filter(user=basic).first()
        duration = 500

        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        response = api_client.get(URL.format(image.uuid, duration))

        assert response.status_code == 403, f'{URL} should return status code 403 for user with invalid permissions'
