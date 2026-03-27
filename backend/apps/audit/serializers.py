from rest_framework import serializers

from apps.audit.models import AuditLog


class AuditActorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()


class AuditLogSerializer(serializers.ModelSerializer):
    actor = AuditActorSerializer(read_only=True, allow_null=True)

    class Meta:
        model = AuditLog
        fields = ("id", "event_type", "metadata", "actor", "created_at")
        read_only_fields = fields
