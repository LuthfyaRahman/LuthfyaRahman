"""
Service layer: thin wrappers over Django ORM and audit logging.
"""
import structlog
from django.db import transaction

from .models import AuditLog, GratifikasiRecord

logger = structlog.get_logger(__name__)


def create_record(text: str, value_estimation: float | None = None) -> GratifikasiRecord:
    record = GratifikasiRecord.objects.create(
        text=text,
        value_estimation=value_estimation,
        status=GratifikasiRecord.Status.PENDING_AI,
    )
    _write_audit(record, "RECORD_CREATED", {"text_length": len(text)})
    logger.info("record_created", record_id=record.pk)
    return record


def save_ai_result(
    record_id: int,
    ai_label: str,
    ai_confidence: float,
    ai_source: str,
) -> GratifikasiRecord:
    with transaction.atomic():
        record = GratifikasiRecord.objects.select_for_update().get(pk=record_id)
        record.ai_label = ai_label
        record.ai_confidence = ai_confidence
        record.ai_source = ai_source
        record.status = GratifikasiRecord.Status.WAITING_APPROVAL
        record.save(update_fields=["ai_label", "ai_confidence", "ai_source", "status", "updated_at"])
        _write_audit(
            record,
            "AI_RESULT_SAVED",
            {"ai_label": ai_label, "ai_confidence": ai_confidence, "ai_source": ai_source},
        )
    logger.info("ai_result_saved", record_id=record_id, ai_label=ai_label)
    return record


def _write_audit(record: GratifikasiRecord, action: str, metadata: dict) -> None:
    AuditLog.objects.create(record=record, action=action, metadata=metadata)
