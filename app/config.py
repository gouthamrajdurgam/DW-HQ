from pathlib import Path
import os
from typing import Any, Dict

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
PREFERENCES_PATH = BASE_DIR / "preferences.yaml"


def load_preferences() -> Dict[str, Any]:
    if not PREFERENCES_PATH.exists():
        return {}
    with PREFERENCES_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)
