import uuid

from django.conf import settings
from django.db import models

from apps.requests.constants import (
    RequestPriority,
    RequestSource,
    RequestStatus,
)


class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="requests",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_requests",
    )
    source = models.CharField(
        max_length=32,
        choices=RequestSource.choices,
        default=RequestSource.TEXT,
    )
    raw_text = models.TextField()
    priority = models.CharField(
        max_length=16,
        choices=RequestPriority.choices,
        default=RequestPriority.NORMAL,
    )
    status = models.CharField(
        max_length=32,
        choices=RequestStatus.choices,
        default=RequestStatus.RECEIVED,
    )
    source_reference = models.CharField(max_length=255, blank=True, default="")
    received_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "-created_at"]),
            models.Index(fields=["organization", "status"]),
        ]

    def __str__(self) -> str:
        return f"Request {self.id} ({self.status})"
