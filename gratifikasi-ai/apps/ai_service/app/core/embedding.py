"""
Sentence-Transformers embedding module.
The model is loaded once at startup via a module-level singleton.
"""
from functools import lru_cache

import structlog
from sentence_transformers import SentenceTransformer

from .config import settings

logger = structlog.get_logger(__name__)


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    logger.info("loading_embedding_model", model=settings.embedding_model)
    return SentenceTransformer(settings.embedding_model)


def embed(text: str) -> list[float]:
    """Return a unit-normalised embedding vector for *text*."""
    model = _get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()
