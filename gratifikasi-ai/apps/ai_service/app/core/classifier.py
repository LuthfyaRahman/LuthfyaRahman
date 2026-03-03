"""
Classifier stub.

In production this would call a fine-tuned transformer model.
Currently returns a deterministic dummy result so the pipeline is
end-to-end functional without GPU requirements.
"""
import structlog

logger = structlog.get_logger(__name__)

_LABELS = [
    "TIDAK WAJIB LAPOR",
    "WAJIB LAPOR",
    "WAJIB TOLAK",
]


def classify(text: str) -> tuple[str, float]:
    """
    Return (label, confidence).
    Stub: picks a label based on simple keyword heuristics.
    Replace the body with a real transformer inference call.
    """
    text_lower = text.lower()
    if any(kw in text_lower for kw in ("suap", "bribe", "gratif")):
        label, confidence = "WAJIB TOLAK", 0.91
    elif any(kw in text_lower for kw in ("souvenir", "hadiah", "gift")):
        label, confidence = "WAJIB LAPOR", 0.78
    else:
        label, confidence = "TIDAK WAJIB LAPOR", 0.65

    logger.debug("classifier_result", label=label, confidence=confidence)
    return label, confidence
