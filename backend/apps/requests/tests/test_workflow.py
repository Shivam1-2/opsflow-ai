import pytest
from django.urls import reverse

from apps.accounts.constants import UserRole
from apps.audit.constants import AuditEventType
from apps.audit.models import AuditLog
from apps.requests.constants import RequestStatus
from apps.requests.models import Request
from apps.core.exceptions import InvalidStateTransitionError
from apps.requests.services import RequestWorkflowService


@pytest.mark.django_db
def test_valid_transition_succeeds(user_factory):
    user = user_factory(role=UserRole.ADMIN)
    request_obj = Request.objects.create(
        organization=user.organization,
        created_by=user,
        raw_text="Workflow",
        status=RequestStatus.RECEIVED,
    )
    updated = RequestWorkflowService.transition(
        request_obj=request_obj,
        user=user,
        target_status=RequestStatus.PROCESSING,
    )
    assert updated.status == RequestStatus.PROCESSING


@pytest.mark.django_db
def test_invalid_transition_fails(user_factory):
    user = user_factory(role=UserRole.ADMIN)
    request_obj = Request.objects.create(
        organization=user.organization,
        created_by=user,
        raw_text="Workflow",
        status=RequestStatus.RECEIVED,
    )
    with pytest.raises(InvalidStateTransitionError):
        RequestWorkflowService.transition(
            request_obj=request_obj,
            user=user,
            target_status=RequestStatus.COMPLETED,
        )


@pytest.mark.django_db
def test_operator_can_start_processing(user_factory):
    user = user_factory(role=UserRole.OPERATOR)
    request_obj = Request.objects.create(
        organization=user.organization,
        created_by=user,
        raw_text="Workflow",
        status=RequestStatus.RECEIVED,
    )
    updated = RequestWorkflowService.transition(
        request_obj=request_obj,
        user=user,
        target_status=RequestStatus.PROCESSING,
    )
    assert updated.status == RequestStatus.PROCESSING


@pytest.mark.django_db
def test_operator_cannot_skip_to_completed(user_factory):
    user = user_factory(role=UserRole.OPERATOR)
    request_obj = Request.objects.create(
        organization=user.organization,
        created_by=user,
        raw_text="Workflow",
        status=RequestStatus.RECEIVED,
    )
    with pytest.raises(InvalidStateTransitionError):
        RequestWorkflowService.transition(
            request_obj=request_obj,
            user=user,
            target_status=RequestStatus.COMPLETED,
        )


@pytest.mark.django_db
def test_transition_api_records_audit(authenticated_client):
    authenticated_client.user.role = UserRole.ADMIN
    authenticated_client.user.save()
    request_obj = Request.objects.create(
        organization=authenticated_client.user.organization,
        created_by=authenticated_client.user,
        raw_text="Transition",
        status=RequestStatus.RECEIVED,
    )
    response = authenticated_client.post(
        reverse("request-transition", args=[request_obj.id]),
        {"to_status": RequestStatus.PROCESSING},
        format="json",
    )
    assert response.status_code == 200
    assert AuditLog.objects.filter(
        request=request_obj,
        event_type=AuditEventType.PROCESSING_STARTED,
    ).exists()


@pytest.mark.django_db
def test_invalid_transition_api_returns_conflict(authenticated_client):
    authenticated_client.user.role = UserRole.ADMIN
    authenticated_client.user.save()
    request_obj = Request.objects.create(
        organization=authenticated_client.user.organization,
        created_by=authenticated_client.user,
        raw_text="Transition",
        status=RequestStatus.RECEIVED,
    )
    response = authenticated_client.post(
        reverse("request-transition", args=[request_obj.id]),
        {"to_status": RequestStatus.COMPLETED},
        format="json",
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "INVALID_STATE_TRANSITION"


@pytest.mark.django_db
def test_concurrent_transition_guard(user_factory):
    user = user_factory(role=UserRole.ADMIN)
    request_obj = Request.objects.create(
        organization=user.organization,
        created_by=user,
        raw_text="Concurrent",
        status=RequestStatus.RECEIVED,
    )
    Request.objects.filter(pk=request_obj.pk).update(status=RequestStatus.PROCESSING)
    request_obj.refresh_from_db()
    request_obj.status = RequestStatus.RECEIVED
    with pytest.raises(InvalidStateTransitionError):
        RequestWorkflowService.transition(
            request_obj=request_obj,
            user=user,
            target_status=RequestStatus.PROCESSING,
        )
