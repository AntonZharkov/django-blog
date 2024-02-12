import pytest
from api.v1.auth_app.services import AuthAppService
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def auth_service():
    return AuthAppService()
