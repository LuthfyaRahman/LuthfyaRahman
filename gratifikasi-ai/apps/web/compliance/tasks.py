"""
Celery tasks for async AI calls and background jobs.
"""
import structlog
from celery import shared_task
from django.conf import settings
from tenacity import retry, stop_after_attempt, wait_exponential

import httpx

from .services import save_ai_result

logger = structlog.get_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def call_ai_predict(self, record_id: int, text: str) -> dict:
    """
    Call the FastAPI /predict endpoint and persist the result.
    Uses tenacity for retry logic on transient HTTP failures.
    """
    logger.info("calling_ai_predict", record_id=record_id)
    try:
        result = _call_predict_with_retry(text)
    except Exception as exc:
        logger.error("ai_predict_failed", record_id=record_id, error=str(exc))
        raise self.retry(exc=exc)

    save_ai_result(
        record_id=record_id,
        ai_label=result["label"],
        ai_confidence=result["confidence"],
        ai_source=result["source"],
    )
    logger.info("ai_predict_done", record_id=record_id, label=result["label"])
    return result


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    reraise=True,
)
def _call_predict_with_retry(text: str) -> dict:
    ai_url = settings.AI_SERVICE_URL
    with httpx.Client(timeout=30) as client:
        response = client.post(f"{ai_url}/predict", json={"text": text})
        response.raise_for_status()
        return response.json()
