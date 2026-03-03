"""
Qdrant vector database client wrapper.
Handles collection auto-creation and CRUD operations.
"""
import structlog
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from qdrant_client.http.exceptions import UnexpectedResponse

from .config import settings

logger = structlog.get_logger(__name__)

_client: QdrantClient | None = None


def get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(url=settings.qdrant_url)
    return _client


def ensure_collection() -> None:
    """Create the Qdrant collection if it does not already exist."""
    client = get_client()
    try:
        client.get_collection(settings.qdrant_collection)
        logger.info("qdrant_collection_exists", collection=settings.qdrant_collection)
    except (UnexpectedResponse, Exception):
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=qmodels.VectorParams(
                size=settings.qdrant_vector_size,
                distance=qmodels.Distance.COSINE,
            ),
        )
        logger.info("qdrant_collection_created", collection=settings.qdrant_collection)


def search_similar(
    vector: list[float],
    top_k: int | None = None,
) -> list[qmodels.ScoredPoint]:
    """Search the collection and return the top-k scored points."""
    client = get_client()
    k = top_k if top_k is not None else settings.top_k
    results = client.search(
        collection_name=settings.qdrant_collection,
        query_vector=vector,
        limit=k,
        with_payload=True,
    )
    return results


def upsert_vector(point_id: str, vector: list[float], payload: dict) -> None:
    """Insert or update a single vector with payload."""
    client = get_client()
    client.upsert(
        collection_name=settings.qdrant_collection,
        points=[
            qmodels.PointStruct(
                id=point_id,
                vector=vector,
                payload=payload,
            )
        ],
    )
    logger.info("vector_upserted", point_id=point_id)
