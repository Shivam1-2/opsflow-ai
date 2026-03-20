import pytest
from django.urls import reverse

from apps.accounts.constants import UserRole
from apps.audit.constants import AuditEventType
from apps.audit.models import AuditLog
from apps.requests.constants import RequestStatus
from apps.requests.models import Request


@pytest.mark.django_db
def test_audit_list_is_tenant_isolated(user_factory, api_client, organization_factory):
    org_a = organization_factory(name="Org A", slug="org-a")
    org_b = organization_factory(name="Org B", slug="org-b")
    user_a = user_factory(email="a@example.com", organization=org_a)
    user_b = user_factory(email="b@example.com", organization=org_b)
    request_a = Request.objects.create(
        organization=org_a,
        created_by=user_a,
        raw_text="A",
        status=RequestStatus.RECEIVED,
    )
    request_b = Request.objects.create(
        organization=org_b,
        created_by=user_b,
        raw_text="B",
        status=RequestStatus.RECEIVED,
    )
    AuditLog.objects.create(
        organization=org_a,
        request=request_a,
        actor=user_a,
        event_type=AuditEventType.REQUEST_CREATED,
        metadata={},
    )
    AuditLog.objects.create(
        organization=org_b,
        request=request_b,
        actor=user_b,
        event_type=AuditEventType.REQUEST_CREATED,
        metadata={},
    )

    api_client.force_authenticate(user=user_a)
    ok = api_client.get(reverse("request-audit", args=[request_a.id]))
    assert ok.status_code == 200
    assert len(ok.json()["results"]) == 1

    blocked = api_client.get(reverse("request-audit", args=[request_b.id]))
    assert blocked.status_code == 404


@pytest.mark.django_db
def test_unauthenticated_cannot_access_requests(api_client, user_factory):
    user = user_factory()
    request_obj = Request.objects.create(
        organization=user.organization,
        created_by=user,
        raw_text="Protected",
        status=RequestStatus.RECEIVED,
    )
    response = api_client.get(reverse("request-detail", args=[request_obj.id]))
    assert response.status_code in {401, 403}


@pytest.mark.django_db
def test_status_endpoint(authenticated_client):
    authenticated_client.user.role = UserRole.REVIEWER
    authenticated_client.user.save()
    request_obj = Request.objects.create(
        organization=authenticated_client.user.organization,
        created_by=authenticated_client.user,
        raw_text="Status",
        status=RequestStatus.RECEIVED,
    )
    response = authenticated_client.get(reverse("request-status", args=[request_obj.id]))
    assert response.status_code == 200
    assert response.json()["status"] == RequestStatus.RECEIVED
