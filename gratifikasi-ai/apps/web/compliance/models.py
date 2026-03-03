from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GratifikasiRecord(models.Model):
    class Status(models.TextChoices):
        PENDING_AI = "PENDING_AI", "Pending AI Review"
        WAITING_APPROVAL = "WAITING_APPROVAL", "Waiting Approval"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    # Core fields
    text = models.TextField(help_text="Description of the gratification event")
    value_estimation = models.FloatField(
        null=True, blank=True, help_text="Estimated monetary value (IDR)"
    )

    # Workflow
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING_AI, db_index=True
    )

    # AI result
    ai_label = models.CharField(max_length=100, blank=True, default="")
    ai_confidence = models.FloatField(null=True, blank=True)
    ai_source = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="'similarity' or 'classifier'",
    )

    # Human review
    final_label = models.CharField(max_length=100, blank=True, default="")
    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_records",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Gratifikasi Record"
        verbose_name_plural = "Gratifikasi Records"

    def __str__(self) -> str:
        return f"Record #{self.pk} [{self.status}]"


class AuditLog(models.Model):
    record = models.ForeignKey(
        GratifikasiRecord,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=100)
    actor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_actions",
    )
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self) -> str:
        return f"AuditLog: {self.action} on Record #{self.record_id}"
