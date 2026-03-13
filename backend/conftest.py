import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.accounts.constants import UserRole
from apps.organizations.models import Organization

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def organization_factory(db):
    def factory(name="Acme Corporation", slug="acme", **kwargs):
        return Organization.objects.create(name=name, slug=slug, **kwargs)

    return factory


@pytest.fixture
def user_factory(organization_factory, db):
    def factory(
        *,
        email="user@example.com",
        password="dev-password-change-me",
        role=UserRole.OPERATOR,
        organization=None,
        is_active=True,
        **kwargs,
    ):
        org = organization or organization_factory()
        return User.objects.create_user(
            email=email,
            password=password,
            organization=org,
            role=role,
            is_active=is_active,
            **kwargs,
        )

    return factory


@pytest.fixture
def authenticated_client(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client
