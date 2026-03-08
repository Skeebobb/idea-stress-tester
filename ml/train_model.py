from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "ideas.csv"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

def main() -> None:
    df = pd.read_csv(DATA_PATH)

    df = df.dropna(subset=["idea", "category"])
    df["idea"] = df["idea"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df = df[(df["idea"] != "") & (df["category"] != "")]
    df = df.drop_duplicates(subset=["idea", "category"])

    X = df["idea"]
    y = df["category"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2),
                max_features=30000
            )
        ),
        (
            "clf",
            LogisticRegression(
                solver="lbfgs",
                max_iter=3000,
                class_weight="balanced"
            )
        )
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average="macro")
    weighted_f1 = f1_score(y_test, y_pred, average="weighted")
    report = classification_report(y_test, y_pred, output_dict=True)

    ARTIFACTS_DIR.mkdir(exist_ok=True)

    model_path = ARTIFACTS_DIR / "idea_classifier.joblib"
    metrics_path = ARTIFACTS_DIR / "metrics.json"
    label_counts_path = ARTIFACTS_DIR / "label_counts.json"

    joblib.dump(pipeline, model_path)

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "accuracy": accuracy,
                "macro_f1": macro_f1,
                "weighted_f1": weighted_f1,
                "num_samples": int(len(df)),
                "num_classes": int(df["category"].nunique()),
                "classification_report": report
            },
            f,
            ensure_ascii=False,
            indent=2
        )

    with open(label_counts_path, "w", encoding="utf-8") as f:
        json.dump(
            df["category"].value_counts().to_dict(),
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\nTraining complete!")
    print(f"Samples: {len(df)}")
    print(f"Classes: {df['category'].nunique()}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")
    print(f"Weighted F1: {weighted_f1:.4f}")
    print(f"\nModel saved to: {model_path}")
    print(f"Metrics saved to: {metrics_path}")
    print(f"Label counts saved to: {label_counts_path}")

if __name__ == "__main__":
    main()