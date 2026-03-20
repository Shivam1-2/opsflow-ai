from django.db import transaction

from apps.accounts.constants import UserRole
from apps.accounts.models import User
from apps.audit.constants import AuditEventType
from apps.audit.models import AuditLog
from apps.core.exceptions import InvalidStateTransitionError
from apps.requests.constants import ALLOWED_TRANSITIONS, RequestStatus
from apps.requests.models import Request


class RequestWorkflowService:
    OPERATOR_ALLOWED: dict[str, set[str]] = {
        RequestStatus.RECEIVED: {RequestStatus.PROCESSING},
    }

    @classmethod
    def create_request(cls, *, user: User, raw_text: str, priority: str) -> Request:
        with transaction.atomic():
            request_obj = Request.objects.create(
                organization=user.organization,
                created_by=user,
                raw_text=raw_text,
                priority=priority,
                status=RequestStatus.RECEIVED,
            )
            AuditLog.objects.create(
                organization=user.organization,
                request=request_obj,
                actor=user,
                event_type=AuditEventType.REQUEST_CREATED,
                metadata={"status": request_obj.status},
            )
        return request_obj

    @classmethod
    def transition(cls, *, request_obj: Request, user: User, target_status: str) -> Request:
        cls._ensure_transition_allowed(user=user, current=request_obj.status, target=target_status)

        with transaction.atomic():
            locked = Request.objects.select_for_update().get(pk=request_obj.pk)
            if locked.status != request_obj.status:
                raise InvalidStateTransitionError(
                    f"Request state changed concurrently. Current status is {locked.status}."
                )
            cls._ensure_transition_allowed(user=user, current=locked.status, target=target_status)

            previous = locked.status
            locked.status = target_status
            locked.save(update_fields=["status", "updated_at"])

            event_type = AuditEventType.STATUS_CHANGED
            if target_status == RequestStatus.PROCESSING and previous == RequestStatus.RECEIVED:
                event_type = AuditEventType.PROCESSING_STARTED
            elif target_status == RequestStatus.FAILED and previous == RequestStatus.PROCESSING:
                event_type = AuditEventType.PROCESSING_FAILED

            AuditLog.objects.create(
                organization=locked.organization,
                request=locked,
                actor=user,
                event_type=event_type,
                metadata={"from_status": previous, "to_status": target_status},
            )
            return locked

    @classmethod
    def _ensure_transition_allowed(cls, *, user: User, current: str, target: str) -> None:
        allowed_targets = ALLOWED_TRANSITIONS.get(current, set())
        if target not in allowed_targets:
            raise InvalidStateTransitionError(
                f"Request cannot transition from {current} to {target}."
            )
        if user.role == UserRole.ADMIN:
            return
        if user.role == UserRole.OPERATOR:
            operator_targets = cls.OPERATOR_ALLOWED.get(current, set())
            if target in operator_targets:
                return
        raise InvalidStateTransitionError(
            f"Your role cannot transition a request from {current} to {target}."
        )
