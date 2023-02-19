import pytest
from rest_framework.test import APIClient
from tests.data.temp_images import cleanup_images


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    yield
    cleanup_images()


@pytest.fixture(scope="session")
def api_client():
    return APIClient()
