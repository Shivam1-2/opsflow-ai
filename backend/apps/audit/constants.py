from django.db import models


class AuditEventType(models.TextChoices):
    REQUEST_CREATED = "REQUEST_CREATED", "Request created"
    STATUS_CHANGED = "STATUS_CHANGED", "Status changed"
    PROCESSING_STARTED = "PROCESSING_STARTED", "Processing started"
    PROCESSING_FAILED = "PROCESSING_FAILED", "Processing failed"
