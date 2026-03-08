import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "data.json"
OUTPUT_PATH = BASE_DIR / "data" / "ideas.csv"

MIN_SAMPLES_PER_CLASS = 50

EXCLUDED_CATEGORIES = {
    "Productivity",
    "Tech",
    "Web App",
    "SaaS",
}

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for item in data:
    name = str(item.get("Name", "")).strip()
    tagline = str(item.get("Tagline", "")).strip()
    industry = str(item.get("Industry", "")).strip()

    if not industry:
        continue

    if industry in EXCLUDED_CATEGORIES:
        continue

    text = f"{name}. {tagline}".strip()

    if len(text) < 10:
        continue

    rows.append({
        "idea": text,
        "category": industry
    })

df = pd.DataFrame(rows)

df = df.drop_duplicates(subset=["idea", "category"])
df = df.dropna(subset=["idea", "category"])

category_counts = df["category"].value_counts()
valid_categories = category_counts[category_counts >= MIN_SAMPLES_PER_CLASS].index

df = df[df["category"].isin(valid_categories)].copy()

df.to_csv(OUTPUT_PATH, index=False)

print("Saved cleaned dataset to:", OUTPUT_PATH)
print("Dataset shape:", df.shape)
print("\nCategories:")
print(df["category"].value_counts())
print("\nNum classes:", df["category"].nunique())