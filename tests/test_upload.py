class TestUpload:
    def test_unauthorized(self, api_client):
        response = api_client.post('/api/upload', data=None)
        assert response.status_code == 401, '/api/upload/ is not giving 401 for unauthorized users'
