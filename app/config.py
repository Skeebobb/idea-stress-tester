from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "artifacts" / "idea_classifier.joblib"
DATA_PATH = BASE_DIR / "data" / "ideas.csv"
METRICS_PATH = BASE_DIR / "artifacts" / "metrics.json"
LABEL_COUNTS_PATH = BASE_DIR / "artifacts" / "label_counts.json"

DEFAULT_TOP_K_PREDICTIONS = 3
DEFAULT_TOP_K_SIMILAR = 3
MIN_SIMILARITY_THRESHOLD = 0.12
LOW_CONFIDENCE_THRESHOLD = 0.20