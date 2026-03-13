import pytest

from apps.accounts.constants import UserRole


@pytest.mark.django_db
def test_user_belongs_to_organization(user_factory, organization_factory):
    org = organization_factory(name="Tenant Org", slug="tenant-org")
    user = user_factory(email="member@example.com", organization=org)
    assert user.organization_id == org.id


@pytest.mark.django_db
def test_user_role_is_valid(user_factory):
    user = user_factory(role=UserRole.REVIEWER)
    assert user.role == UserRole.REVIEWER


@pytest.mark.django_db
def test_password_is_hashed(user_factory):
    user = user_factory(password="plain-text-password")
    assert user.password != "plain-text-password"
    assert user.check_password("plain-text-password")
