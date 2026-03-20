import pytest
from django.urls import reverse

from apps.accounts.constants import UserRole
from apps.audit.constants import AuditEventType
from apps.audit.models import AuditLog
from apps.requests.constants import RequestPriority, RequestSource, RequestStatus
from apps.requests.models import Request


@pytest.mark.django_db
def test_operator_can_create_request(authenticated_client):
    authenticated_client.user.role = UserRole.OPERATOR
    authenticated_client.user.save()
    response = authenticated_client.post(
        reverse("request-list-create"),
        {"raw_text": "Please change Acme Corp's subscription from monthly to annual."},
        format="json",
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == RequestStatus.RECEIVED
    assert body["source"] == RequestSource.TEXT
    assert body["priority"] == RequestPriority.NORMAL
    assert "monthly to annual" in body["raw_text"]

    request_obj = Request.objects.get(pk=body["id"])
    assert request_obj.organization_id == authenticated_client.user.organization_id
    assert request_obj.created_by_id == authenticated_client.user.id


@pytest.mark.django_db
def test_create_request_rejects_empty_text(authenticated_client):
    authenticated_client.user.role = UserRole.OPERATOR
    authenticated_client.user.save()
    response = authenticated_client.post(
        reverse("request-list-create"),
        {"raw_text": "   "},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_reviewer_cannot_create_request(authenticated_client):
    authenticated_client.user.role = UserRole.REVIEWER
    authenticated_client.user.save()
    response = authenticated_client.post(
        reverse("request-list-create"),
        {"raw_text": "Need a change."},
        format="json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_returns_only_organization_requests(user_factory, api_client, organization_factory):
    org_a = organization_factory(name="Org A", slug="org-a")
    org_b = organization_factory(name="Org B", slug="org-b")
    user_a = user_factory(email="a@example.com", organization=org_a)
    user_b = user_factory(email="b@example.com", organization=org_b)

    Request.objects.create(
        organization=org_a,
        created_by=user_a,
        raw_text="Org A request",
        status=RequestStatus.RECEIVED,
    )
    Request.objects.create(
        organization=org_b,
        created_by=user_b,
        raw_text="Org B request",
        status=RequestStatus.RECEIVED,
    )

    api_client.force_authenticate(user=user_a)
    response = api_client.get(reverse("request-list-create"))
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 1
    assert results[0]["id"] is not None


@pytest.mark.django_db
def test_detail_cross_tenant_returns_not_found(user_factory, api_client, organization_factory):
    org_a = organization_factory(name="Org A", slug="org-a")
    org_b = organization_factory(name="Org B", slug="org-b")
    user_a = user_factory(email="a@example.com", organization=org_a)
    user_b = user_factory(email="b@example.com", organization=org_b)
    foreign_request = Request.objects.create(
        organization=org_b,
        created_by=user_b,
        raw_text="Secret",
        status=RequestStatus.RECEIVED,
    )

    api_client.force_authenticate(user=user_a)
    response = api_client.get(reverse("request-detail", args=[foreign_request.id]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_client_cannot_set_status_on_create(authenticated_client):
    authenticated_client.user.role = UserRole.OPERATOR
    authenticated_client.user.save()
    response = authenticated_client.post(
        reverse("request-list-create"),
        {
            "raw_text": "Valid text",
            "status": RequestStatus.COMPLETED,
            "organization": "00000000-0000-0000-0000-000000000099",
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["status"] == RequestStatus.RECEIVED


@pytest.mark.django_db
def test_request_creation_writes_audit_event(authenticated_client):
    authenticated_client.user.role = UserRole.OPERATOR
    authenticated_client.user.save()
    response = authenticated_client.post(
        reverse("request-list-create"),
        {"raw_text": "Audit me"},
        format="json",
    )
    request_id = response.json()["id"]
    assert AuditLog.objects.filter(
        request_id=request_id,
        event_type=AuditEventType.REQUEST_CREATED,
    ).exists()
