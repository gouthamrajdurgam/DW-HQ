import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
CSV_PATH = DATA_DIR / "feedback.csv"


def ensure_feedback_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["listing_id", "label", "features_json", "created_at"])


def add_feedback(listing_id: str, label: int, features: Dict[str, float]) -> None:
    ensure_feedback_file()
    with CSV_PATH.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            listing_id,
            label,
            json.dumps(features),
            datetime.utcnow().isoformat(),
        ])


def load_feedback() -> List[Dict[str, str]]:
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))
