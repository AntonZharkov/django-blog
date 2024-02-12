from base64 import b64decode

import pytest
from blog.models import Category
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import Client
from django.test.utils import override_settings
from rest_framework_simplejwt.tokens import RefreshToken

pytestmark = [pytest.mark.django_db]

User = get_user_model()

locmem_email_backend = override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CELERY_TASK_ALWAYS_EAGER=True,
)

raw_image: str = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAA"
    "AA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjYAAAAAIAAeIhvDMAAAAASUVORK5CYII="
)


@pytest.fixture
def image_content_file() -> ContentFile:
    _format, _raw_image = raw_image.split(";base64,")
    extention = _format.split("/")[1]
    return ContentFile(b64decode(_raw_image), f"image.{extention}")


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        email="q@gmail.com",
        password="12345678",
        is_active=True,
        first_name="Anton",
        last_name="Zharkov",
    )


@pytest.fixture
def second_user() -> User:
    return User.objects.create_user(
        email="second@gmail.com",
        password="12345678",
        is_active=True,
        first_name="User2",
        last_name="Second",
    )


@pytest.fixture
def user_with_following_followers(second_user: User, user: User) -> User:
    user.following.add(second_user)
    second_user.following.add(user)
    return user


@pytest.fixture
def second_user_with_following_followers(second_user: User, user: User) -> User:
    second_user.following.add(user)
    user.following.add(second_user)
    return second_user


@pytest.fixture
def user_token(user) -> tuple[str, str]:
    refresh = RefreshToken().for_user(user)
    return str(refresh), refresh.access_token


@pytest.fixture
def api_client(client, user_token) -> Client:
    # client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {user_token[1]}'
    client.cookies["jwt-auth"] = user_token[1]
    client.cookies["refresh"] = user_token[0]
    return client


@pytest.fixture
def category() -> Category:
    return Category.objects.create(name="Test1")
