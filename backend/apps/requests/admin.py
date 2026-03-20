from django.contrib import admin

from apps.requests.models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "status", "priority", "created_by", "created_at")
    list_filter = ("status", "priority", "organization")
    search_fields = ("id", "raw_text")
    readonly_fields = ("created_at", "updated_at")
