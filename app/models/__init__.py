import json
import random
import time
from typing import Any, Dict, List


def unique_by_url(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique_items = []
    for item in items:
        url = item.get("url")
        if not url:
            continue
        if url in seen:
            continue
        seen.add(url)
        unique_items.append(item)
    return unique_items


def random_delay(min_s: float = 1.0, max_s: float = 4.0) -> None:
    time.sleep(random.uniform(min_s, max_s))


def normalize_price(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    raw = str(value).replace("€", "").replace(".", "").replace(" ", "")
    raw = raw.replace(",", ".")
    try:
        return float(raw)
    except ValueError:
        return 0.0


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value).replace(" ", "")))
    except Exception:
        return default
