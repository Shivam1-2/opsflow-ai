import uuid

from django.conf import settings
from django.db import models

from apps.audit.constants import AuditEventType
from apps.organizations.models import Organization


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )
    request = models.ForeignKey(
        "requests.Request",
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events",
    )
    event_type = models.CharField(max_length=64, choices=AuditEventType.choices)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["organization", "request", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.event_type} ({self.request_id})"
