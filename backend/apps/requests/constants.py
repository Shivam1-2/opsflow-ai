from django.db import models


class RequestSource(models.TextChoices):
    TEXT = "TEXT", "Text"
    DOCUMENT = "DOCUMENT", "Document"


class RequestPriority(models.TextChoices):
    LOW = "LOW", "Low"
    NORMAL = "NORMAL", "Normal"
    HIGH = "HIGH", "High"
    URGENT = "URGENT", "Urgent"


class RequestStatus(models.TextChoices):
    RECEIVED = "RECEIVED", "Received"
    PROCESSING = "PROCESSING", "Processing"
    EXTRACTED = "EXTRACTED", "Extracted"
    VALIDATING = "VALIDATING", "Validating"
    PENDING_REVIEW = "PENDING_REVIEW", "Pending review"
    FAILED = "FAILED", "Failed"
    REJECTED = "REJECTED", "Rejected"
    APPROVED = "APPROVED", "Approved"
    EXECUTING = "EXECUTING", "Executing"
    COMPLETED = "COMPLETED", "Completed"


ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    RequestStatus.RECEIVED: {RequestStatus.PROCESSING},
    RequestStatus.PROCESSING: {RequestStatus.EXTRACTED, RequestStatus.FAILED},
    RequestStatus.EXTRACTED: {RequestStatus.VALIDATING},
    RequestStatus.VALIDATING: {RequestStatus.PENDING_REVIEW, RequestStatus.FAILED},
    RequestStatus.PENDING_REVIEW: {RequestStatus.APPROVED, RequestStatus.REJECTED},
    RequestStatus.APPROVED: {RequestStatus.EXECUTING},
    RequestStatus.EXECUTING: {RequestStatus.COMPLETED, RequestStatus.FAILED},
    RequestStatus.FAILED: set(),
    RequestStatus.REJECTED: set(),
    RequestStatus.COMPLETED: set(),
}

MAX_RAW_TEXT_LENGTH = 20_000
