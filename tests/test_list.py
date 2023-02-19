import pytest
from hexOceanBackend.settings import DEBUG
from tests.data.temp_users import TempUsers
from tests.data.temp_images import TempImages

URL = '/api/list/{0}'


class TestList:
    @pytest.mark.xfail(condition=DEBUG, reason='Switching unauthorized users to users.TestUser if DEBUG is True')
    def test_unauthorized(self, api_client):
        response = api_client.post(URL.format(1), data=None)
        assert response.status_code == 401, f'{URL} is not giving 401 for unauthorized users'

    def test_different_permissions(self, api_client):
        TempUsers.populate_users()
        TempImages.populate_images(api_client)

        # Basic user
        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        response = api_client.get(URL.format(1))

        assert response.status_code == 200, f'{URL} not giving status 200'
        assert len(response.data['data'][0]['thumbnails']) == 1, f'{URL} is not giving 1 thumbnail to basic user'
        assert response.data['data'][0].get('original') is None, f'{URL} is giving original link to basic user'

        api_client.logout()

        # Premium user
        api_client.login(username=TempUsers.premium['username'], password=TempUsers.premium['password'])
        response = api_client.get(URL.format(1))

        assert response.status_code == 200, f'{URL} not giving status 200'
        assert len(response.data['data'][0]['thumbnails']) == 2, f'{URL} is not giving 2 thumbnail to premium user'
        assert response.data['data'][0].get('original') is not None, f'{URL} is not giving original link to prem. user'

        api_client.logout()

        # Enterprise user
        api_client.login(username=TempUsers.enterprise['username'], password=TempUsers.enterprise['password'])
        response = api_client.get(URL.format(1))

        assert response.status_code == 200, f'{URL} not giving status 200'
        assert len(response.data['data'][0]['thumbnails']) == 2, f'{URL} is not giving 2 thumbnail to ent. user'
        assert response.data['data'][0].get('original') is not None, f'{URL} is not giving original link to ent. user'

    def test_no_images(self, api_client):
        TempUsers.populate_users()
        api_client.login(username=TempUsers.basic['username'], password=TempUsers.basic['password'])
        response = api_client.get(URL.format(1))

        assert response.status_code == 200, f'{URL} not giving status 200'
        assert response.data['pages']['current'] == 1, f'Current page for user without pictures is not equal to 1'
        assert response.data['pages']['previous'] is None, f'Previous page for user without pictures is not None'
        assert response.data['pages']['next'] is None, f'Next page for user without pictures is not None'
        assert len(response.data['data']) == 0, f'Response data is not empty for user without pictures'