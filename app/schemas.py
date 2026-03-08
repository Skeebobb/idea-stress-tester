from pydantic import BaseModel, Field


class IdeaRequest(BaseModel):
    idea: str = Field(..., max_length=500)


class PredictionItem(BaseModel):
    category: str
    probability: float


class BusinessSignals(BaseModel):
    has_ai: bool
    has_api: bool
    has_marketplace: bool
    has_platform: bool
    has_b2b_hint: bool
    has_b2c_hint: bool
    has_subscription_hint: bool
    has_analytics_hint: bool


class SimilarIdea(BaseModel):
    idea: str
    category: str
    similarity: float


class IdeaResponse(BaseModel):
    input_idea: str
    is_valid_idea: bool
    validation_message: str | None
    predicted_category: str
    confidence: float
    low_confidence: bool
    clarity_score: float
    idea_score: float
    competition_level: str
    business_signals: BusinessSignals
    top_predictions: list[PredictionItem]
    similar_ideas: list[SimilarIdea]
    strengths: list[str]
    risks: list[str]
    recommendations: list[str]


class CategoryItem(BaseModel):
    category: str
    count: int


class ModelInfoResponse(BaseModel):
    accuracy: float
    macro_f1: float
    weighted_f1: float
    num_samples: int
    num_classes: int
    classification_report: dict