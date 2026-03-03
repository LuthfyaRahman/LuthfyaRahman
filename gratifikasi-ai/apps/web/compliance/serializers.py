from rest_framework import serializers

from .models import AuditLog, GratifikasiRecord


class GratifikasiRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GratifikasiRecord
        fields = [
            "id",
            "text",
            "value_estimation",
            "status",
            "ai_label",
            "ai_confidence",
            "ai_source",
            "final_label",
            "approved_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "ai_label",
            "ai_confidence",
            "ai_source",
            "created_at",
            "updated_at",
        ]


class GratifikasiSubmitSerializer(serializers.ModelSerializer):
    """Accepts only user-supplied fields on submission."""

    class Meta:
        model = GratifikasiRecord
        fields = ["text", "value_estimation"]


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ["id", "record", "action", "actor", "metadata", "timestamp"]
