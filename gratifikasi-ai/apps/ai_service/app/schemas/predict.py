from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to classify")


class PredictResponse(BaseModel):
    label: str
    confidence: float
    source: str  # "similarity" | "classifier"
    matched_payload: dict | None = None


class UpsertRequest(BaseModel):
    case_id: str = Field(..., description="Unique case identifier")
    text: str = Field(..., min_length=1)
    label: str
    metadata: dict = Field(default_factory=dict)


class UpsertResponse(BaseModel):
    case_id: str
    status: str = "upserted"
