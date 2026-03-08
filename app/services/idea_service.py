import json

from app.config import LABEL_COUNTS_PATH, METRICS_PATH
from app.predictor import IdeaPredictor


class IdeaAnalysisService:
    def __init__(self) -> None:
        self.predictor = IdeaPredictor()

    def analyze_idea(self, idea: str) -> dict:
        return self.predictor.predict(idea, top_k=3)

    def get_model_info(self) -> dict:
        if not METRICS_PATH.exists():
            raise FileNotFoundError("metrics.json not found. Train the model first.")

        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_categories(self) -> list[dict]:
        if not LABEL_COUNTS_PATH.exists():
            raise FileNotFoundError("label_counts.json not found. Train the model first.")

        with open(LABEL_COUNTS_PATH, "r", encoding="utf-8") as f:
            label_counts = json.load(f)

        return [
            {"category": category, "count": count}
            for category, count in sorted(label_counts.items(), key=lambda x: x[0].lower())
        ]