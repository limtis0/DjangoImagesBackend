import pytest
from rest_framework.test import APIClient
from tests.data.temp_images import TempImages


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    yield
    TempImages.cleanup_images()


@pytest.fixture(scope="session")
def api_client():
    return APIClient()
