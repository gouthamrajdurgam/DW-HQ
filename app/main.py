import csv
import json
from pathlib import Path
from typing import Dict, List

from sklearn.linear_model import LinearRegression

from app.models.feature_builder import feature_columns

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def load_feedback_rows() -> List[Dict[str, float]]:
    path = DATA_DIR / "feedback.csv"
    if not path.exists():
        return []

    rows: List[Dict[str, float]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("listing_id"):
                continue
            try:
                features = json.loads(row.get("features_json", "{}"))
            except Exception:
                features = {}
            rows.append({"features": features, "label": float(row.get("label", 0))})
    return rows


def train_model_from_feedback() -> LinearRegression:
    rows = load_feedback_rows()
    if not rows:
        model = LinearRegression()
        model.fit([[0.0] * len(feature_columns())], [0.0])
        return model

    X = []
    y = []
    for row in rows:
        feature_values = [row["features"].get(col, 0.0) for col in feature_columns()]
        X.append(feature_values)
        y.append(float(row["label"]))

    model = LinearRegression()
    model.fit(X, y)
    return model
