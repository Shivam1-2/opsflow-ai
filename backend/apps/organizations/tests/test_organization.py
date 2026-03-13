import pytest

from apps.organizations.models import Organization


@pytest.mark.django_db
def test_organization_can_be_created():
    org = Organization.objects.create(name="Acme Corporation", slug="acme")
    assert org.id is not None
    assert org.name == "Acme Corporation"


@pytest.mark.django_db
def test_organization_slug_is_unique():
    Organization.objects.create(name="Acme", slug="acme")
    with pytest.raises(Exception):
        Organization.objects.create(name="Other", slug="acme")
