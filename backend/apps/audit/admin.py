from django.contrib import admin

from apps.audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("event_type", "request", "organization", "actor", "created_at")
    list_filter = ("event_type", "organization")
    readonly_fields = ("organization", "request", "actor", "event_type", "metadata", "created_at")
