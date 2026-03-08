from pathlib import Path
from typing import Any
import re

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "artifacts" / "idea_classifier.joblib"
DATA_PATH = BASE_DIR / "data" / "ideas.csv"


class IdeaPredictor:
    def __init__(self) -> None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}. Run train_model.py first."
            )
        if not DATA_PATH.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {DATA_PATH}. Run prepare_dataset.py first."
            )

        self.pipeline = joblib.load(MODEL_PATH)
        self.dataset = pd.read_csv(DATA_PATH).dropna(subset=["idea", "category"]).copy()
        self.dataset["idea"] = self.dataset["idea"].astype(str).str.strip()
        self.dataset["category"] = self.dataset["category"].astype(str).str.strip()
        self.dataset = self.dataset[
            (self.dataset["idea"] != "") & (self.dataset["category"] != "")
        ].drop_duplicates(subset=["idea", "category"])

        self.vectorizer = self.pipeline.named_steps["tfidf"]
        self.dataset_vectors = self.vectorizer.transform(self.dataset["idea"])

    def _validate_input_text(self, text: str) -> tuple[bool, str | None]:
        cleaned = text.strip()

        if not cleaned:
            return False, "Please enter an idea description."

        if len(cleaned) < 12:
            return False, "The idea is too short. Please describe it in a bit more detail."

        words = cleaned.split()
        if len(words) < 3:
            return False, "Please use at least 3 words to describe the idea."

        letters = re.findall(r"[A-Za-z]", cleaned)
        if len(letters) < 6:
            return False, "The input does not look like a meaningful product idea."

        alnum_chars = re.findall(r"[A-Za-z0-9]", cleaned)
        if not alnum_chars:
            return False, "The input does not look like a meaningful product idea."

        vowel_count = len(re.findall(r"[AEIOUaeiou]", cleaned))
        letter_ratio = len(letters) / max(len(cleaned), 1)

        if len(words) == 1 and len(cleaned) > 10:
            return False, "This looks like random text. Please describe a product or startup idea."

        if letter_ratio < 0.45:
            return False, "The input looks noisy. Please describe the idea using normal words."

        if vowel_count == 0:
            return False, "The input does not look like a meaningful idea description."

        return True, None

    def _calculate_clarity_score(self, text: str, confidence: float) -> float:
        word_count = len(text.split())
        score = 0.0

        if word_count >= 6:
            score += 2.5
        if word_count >= 10:
            score += 2.0
        if word_count >= 16:
            score += 1.5

        score += min(confidence * 20, 4.0)

        return round(min(score, 10.0), 2)

    def _extract_business_signals(self, text: str) -> dict[str, bool]:
        lowered = text.lower()

        return {
            "has_ai": any(word in lowered for word in ["ai", "artificial intelligence", "ml"]),
            "has_api": "api" in lowered,
            "has_marketplace": "marketplace" in lowered,
            "has_platform": "platform" in lowered,
            "has_b2b_hint": any(
                phrase in lowered for phrase in ["for teams", "for businesses", "for companies"]
            ),
            "has_b2c_hint": any(
                phrase in lowered for phrase in ["for students", "for families", "for creators", "for users"]
            ),
            "has_subscription_hint": any(
                phrase in lowered for phrase in ["subscription", "monthly", "paid plan"]
            ),
            "has_analytics_hint": "analytics" in lowered,
        }

    def _competition_level(self, predicted_category: str) -> str:
        high_competition = {
            "Artificial Intelligence",
            "Marketing",
            "Design Tools",
            "Fintech",
            "Social Media",
            "Analytics",
        }

        medium_competition = {
            "Education",
            "Writing",
            "Email",
            "Sales",
            "Health & Fitness",
            "Hiring",
        }

        if predicted_category in high_competition:
            return "high"
        if predicted_category in medium_competition:
            return "medium"
        return "low"

    def _calculate_idea_score(
        self,
        confidence: float,
        text: str,
        predicted_category: str,
        business_signals: dict[str, bool],
    ) -> float:
        score = 0.0

        score += min(confidence * 25, 2.5)

        word_count = len(text.split())
        if word_count >= 6:
            score += 1.0
        if word_count >= 10:
            score += 1.0
        if word_count >= 15:
            score += 1.0

        signal_count = sum(business_signals.values())
        score += min(signal_count * 0.5, 2.0)

        specific_categories = {
            "Fintech",
            "Health & Fitness",
            "Hiring",
            "Email",
            "Analytics",
            "Developer Tools",
            "Education",
            "Writing",
            "API",
        }
        if predicted_category in specific_categories:
            score += 0.5

        if confidence < 0.08:
            score -= 1.5
        elif confidence < 0.12:
            score -= 1.0
        elif confidence < 0.18:
            score -= 0.5

        return round(max(0.0, min(score, 10.0)), 2)

    def _generate_strengths(
        self,
        confidence: float,
        business_signals: dict[str, bool],
        predicted_category: str,
    ) -> list[str]:
        strengths: list[str] = []

        if confidence >= 0.2:
            strengths.append("Idea is relatively well-defined for the classifier.")
        if business_signals["has_ai"]:
            strengths.append("Includes an AI angle, which may increase product appeal.")
        if business_signals["has_api"]:
            strengths.append("API component suggests integration potential.")
        if business_signals["has_marketplace"]:
            strengths.append("Marketplace structure can support network effects.")
        if business_signals["has_b2b_hint"]:
            strengths.append("Clear B2B audience signal detected.")
        if predicted_category in {"Developer Tools", "Analytics", "API"}:
            strengths.append("Category is relatively concrete and easier to position.")

        if not strengths:
            strengths.append("The idea has a recognizable product direction.")

        return strengths[:3]

    def _generate_risks(
        self,
        confidence: float,
        competition_level: str,
        text: str,
        business_signals: dict[str, bool],
    ) -> list[str]:
        risks: list[str] = []

        if confidence < 0.12:
            risks.append("The idea description is vague, so positioning may be unclear.")
        if competition_level == "high":
            risks.append("This category appears highly competitive.")
        if len(text.split()) < 8:
            risks.append("The idea may need more detail about user and use case.")
        if not business_signals["has_b2b_hint"] and not business_signals["has_b2c_hint"]:
            risks.append("Target audience is not clearly specified.")
        if not business_signals["has_subscription_hint"] and not business_signals["has_marketplace"]:
            risks.append("Monetization approach is not obvious from the description.")

        if not risks:
            risks.append("Execution quality and differentiation will matter a lot.")

        return risks[:3]

    def _generate_recommendations(
        self,
        confidence: float,
        text: str,
        business_signals: dict[str, bool],
        competition_level: str,
    ) -> list[str]:
        recommendations: list[str] = []

        if confidence < 0.12:
            recommendations.append(
                "Make the idea more specific by clearly describing the target user and core value proposition."
            )

        if not business_signals["has_b2b_hint"] and not business_signals["has_b2c_hint"]:
            recommendations.append(
                "Specify the target audience more clearly, for example students, teams, or small businesses."
            )

        if not business_signals["has_subscription_hint"] and not business_signals["has_marketplace"]:
            recommendations.append(
                "Add a clearer monetization model such as subscription, commission, or paid plan."
            )

        if competition_level == "high":
            recommendations.append(
                "Differentiate the product with a niche focus or a unique workflow advantage."
            )

        if len(text.split()) < 10:
            recommendations.append(
                "Describe the product in more detail, including the use case and expected outcome for users."
            )

        if not recommendations:
            recommendations.append(
                "The idea is reasonably structured; focus next on differentiation and market validation."
            )

        return recommendations[:3]

    def _find_similar_ideas(self, text: str, top_k: int = 3) -> list[dict[str, Any]]:
        query_vector = self.vectorizer.transform([text])
        similarities = cosine_similarity(query_vector, self.dataset_vectors)[0]

        ranked_indices = np.argsort(similarities)[::-1]

        results: list[dict[str, Any]] = []
        seen_ideas: set[str] = set()

        for idx in ranked_indices:
            similarity = float(similarities[idx])
            if similarity < 0.12:
                continue

            row = self.dataset.iloc[idx]
            idea_text = str(row["idea"]).strip()

            if idea_text.lower() == text.lower():
                continue

            if idea_text in seen_ideas:
                continue

            results.append(
                {
                    "idea": idea_text,
                    "category": str(row["category"]),
                    "similarity": round(similarity, 4),
                }
            )
            seen_ideas.add(idea_text)

            if len(results) >= top_k:
                break

        return results

    def predict(self, text: str, top_k: int = 3) -> dict[str, Any]:
        text = text.strip()

        is_valid_idea, validation_message = self._validate_input_text(text)

        if not is_valid_idea:
            return {
                "input_idea": text,
                "is_valid_idea": False,
                "validation_message": validation_message,
                "predicted_category": "Unknown",
                "confidence": 0.0,
                "low_confidence": True,
                "clarity_score": 0.0,
                "idea_score": 0.0,
                "competition_level": "unknown",
                "business_signals": {
                    "has_ai": False,
                    "has_api": False,
                    "has_marketplace": False,
                    "has_platform": False,
                    "has_b2b_hint": False,
                    "has_b2c_hint": False,
                    "has_subscription_hint": False,
                    "has_analytics_hint": False,
                },
                "top_predictions": [],
                "similar_ideas": [],
                "strengths": [],
                "risks": ["The input is too weak for reliable analysis."],
                "recommendations": [
                    "Describe the product, target user, and core value more clearly."
                ],
            }

        probs = self.pipeline.predict_proba([text])[0]
        classes = self.pipeline.classes_

        best_idx = int(np.argmax(probs))
        best_prob = float(probs[best_idx])
        predicted_category = str(classes[best_idx])

        extremely_low_confidence = best_prob < 0.07

        top_indices = np.argsort(probs)[::-1][:top_k]
        top_predictions = [
            {
                "category": str(classes[idx]),
                "probability": round(float(probs[idx]), 4),
            }
            for idx in top_indices
        ]

        business_signals = self._extract_business_signals(text)
        competition_level = self._competition_level(predicted_category)
        clarity_score = self._calculate_clarity_score(text, best_prob)
        idea_score = self._calculate_idea_score(
            confidence=best_prob,
            text=text,
            predicted_category=predicted_category,
            business_signals=business_signals,
        )
        strengths = self._generate_strengths(best_prob, business_signals, predicted_category)
        risks = self._generate_risks(best_prob, competition_level, text, business_signals)
        recommendations = self._generate_recommendations(
            confidence=best_prob,
            text=text,
            business_signals=business_signals,
            competition_level=competition_level,
        )
        similar_ideas = self._find_similar_ideas(text, top_k=3)

        if extremely_low_confidence:
            risks.insert(0, "The model is very uncertain about this idea classification.")
            recommendations.insert(
                0,
                "Add more detail about the user, problem, and product workflow to improve analysis quality.",
            )

        return {
            "input_idea": text,
            "is_valid_idea": True,
            "validation_message": None,
            "predicted_category": predicted_category,
            "confidence": round(best_prob, 4),
            "low_confidence": best_prob < 0.2,
            "clarity_score": clarity_score,
            "idea_score": idea_score,
            "competition_level": competition_level,
            "business_signals": business_signals,
            "top_predictions": top_predictions,
            "similar_ideas": similar_ideas,
            "strengths": strengths,
            "risks": risks[:4],
            "recommendations": recommendations[:4],
        }