import structlog
from fastapi import APIRouter

from ..core import classifier, embedding, qdrant_wrapper
from ..core.config import settings
from ..schemas.predict import (
    PredictRequest,
    PredictResponse,
    UpsertRequest,
    UpsertResponse,
)

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest) -> PredictResponse:
    """
    1. Generate embedding for the input text.
    2. Search Qdrant for similar vectors.
    3. If best similarity >= threshold → return similarity result.
    4. Else → run classifier stub.
    """
    vector = embedding.embed(request.text)
    results = qdrant_wrapper.search_similar(vector, top_k=settings.top_k)

    if results and results[0].score >= settings.similarity_threshold:
        top = results[0]
        label = top.payload.get("label", "UNKNOWN")
        logger.info(
            "predict_via_similarity",
            score=top.score,
            label=label,
        )
        return PredictResponse(
            label=label,
            confidence=round(top.score, 4),
            source="similarity",
            matched_payload=top.payload,
        )

    # Fall back to classifier
    label, confidence = classifier.classify(request.text)
    logger.info("predict_via_classifier", label=label, confidence=confidence)
    return PredictResponse(
        label=label,
        confidence=round(confidence, 4),
        source="classifier",
    )


@router.post("/cases/upsert", response_model=UpsertResponse)
async def upsert_case(request: UpsertRequest) -> UpsertResponse:
    """Store a labelled case embedding into Qdrant."""
    vector = embedding.embed(request.text)
    payload = {"label": request.label, "text": request.text, **request.metadata}
    qdrant_wrapper.upsert_vector(
        point_id=request.case_id,
        vector=vector,
        payload=payload,
    )
    return UpsertResponse(case_id=request.case_id)
