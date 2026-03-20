from rest_framework import serializers

from apps.requests.constants import MAX_RAW_TEXT_LENGTH, RequestPriority, RequestStatus
from apps.requests.models import Request


class RequestCreateSerializer(serializers.Serializer):
    raw_text = serializers.CharField(max_length=MAX_RAW_TEXT_LENGTH, trim_whitespace=False)
    priority = serializers.ChoiceField(
        choices=RequestPriority.choices,
        required=False,
        default=RequestPriority.NORMAL,
    )

    def validate_raw_text(self, value: str) -> str:
        if not value or not value.strip():
            raise serializers.ValidationError("Request text cannot be empty.")
        return value


class UserSummarySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()


class RequestListSerializer(serializers.ModelSerializer):
    created_by = UserSummarySerializer(read_only=True)

    class Meta:
        model = Request
        fields = (
            "id",
            "source",
            "priority",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class RequestDetailSerializer(serializers.ModelSerializer):
    created_by = UserSummarySerializer(read_only=True)

    class Meta:
        model = Request
        fields = (
            "id",
            "source",
            "raw_text",
            "priority",
            "status",
            "created_by",
            "source_reference",
            "received_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ("id", "status", "updated_at")
        read_only_fields = fields


class RequestTransitionSerializer(serializers.Serializer):
    to_status = serializers.ChoiceField(choices=RequestStatus.choices)
