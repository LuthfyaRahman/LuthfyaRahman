from django.contrib import admin

from .models import AuditLog, GratifikasiRecord


@admin.register(GratifikasiRecord)
class GratifikasiRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "ai_label",
        "ai_confidence",
        "ai_source",
        "final_label",
        "approved_by",
        "created_at",
    )
    list_filter = ("status", "ai_source")
    search_fields = ("text", "ai_label", "final_label")
    readonly_fields = (
        "ai_label",
        "ai_confidence",
        "ai_source",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "record", "action", "actor", "timestamp")
    list_filter = ("action",)
    readonly_fields = ("record", "action", "actor", "metadata", "timestamp")
    ordering = ("-timestamp",)
